import os
import datetime
import re
import time
import json
import beaupy
import pandas as pd
from typing import List, Dict, Optional, Any, Tuple

# --- DEPENDÊNCIAS ---
# pip install requests beaupy pandas
import requests

# --- CONFIGURAÇÕES ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_SOURCE_DIR = os.path.join(SCRIPT_DIR, "Json_CyberMetrics")
RESULTS_ROOT_DIR = os.path.join(SCRIPT_DIR, "ResultsCyberMetrics")

OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_TAGS_ENDPOINT_SUFFIX = "/tags"
OLLAMA_GENERATE_ENDPOINT_SUFFIX = "/generate"
OLLAMA_REQUEST_TIMEOUT_SECONDS = 700
OLLAMA_KEEP_ALIVE_DURATION = "5m"

LOG_DIR_NAME = "cybersecurity_test_logs"

# --- FUNÇÕES AUXILIARES ---

def list_ollama_models() -> List[str]:
    """Lista todos os modelos disponíveis no Ollama."""
    try:
        response = requests.get(f"{OLLAMA_API_BASE_URL}{OLLAMA_TAGS_ENDPOINT_SUFFIX}", timeout=10)
        response.raise_for_status()
        models = [model["name"] for model in response.json().get("models", [])]
        if not models: raise ValueError("No models found")
        models.sort()
        return models
    except Exception as e:
        print(f"[ERROR] Could not fetch models from Ollama: {e}")
        return []

def call_ollama(model_name: str, user_prompt: str, system_prompt: str) -> Tuple[str, Optional[str], float]:
    """Chama a API Ollama e extrai a letra da resposta (A-E) ou a resposta completa."""
    payload = {"model": model_name, "system": system_prompt, "prompt": user_prompt, "stream": False, "keep_alive": OLLAMA_KEEP_ALIVE_DURATION}
    start_time = time.perf_counter()
    try:
        response = requests.post(f"{OLLAMA_API_BASE_URL}{OLLAMA_GENERATE_ENDPOINT_SUFFIX}", json=payload, timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        response_data = response.json()
        duration = time.perf_counter() - start_time
        full_response = response_data.get("response", "Error: No 'response' key in Ollama's output.").strip()
        
        strong_pattern_match = re.search(r'(?:answer is|answer:)\s*\**\s*\b([A-E])\b', full_response, re.IGNORECASE)
        if strong_pattern_match:
            extracted_answer = strong_pattern_match.group(1).upper()
        else:
            all_standalone_letters = re.findall(r'\b([A-E])\b', full_response, re.IGNORECASE)
            extracted_answer = all_standalone_letters[-1].upper() if all_standalone_letters else full_response
        return full_response, extracted_answer, duration
    except Exception as e:
        duration = time.perf_counter() - start_time
        error_msg = f"Error: Request to Ollama failed: {e}"
        return error_msg, error_msg, duration

def find_json_files(source_dir: str) -> List[str]:
    """Procura por ficheiros .json num diretório e retorna os seus caminhos completos."""
    if not os.path.isdir(source_dir):
        print(f"[ERROR] O diretório de origem '{source_dir}' não foi encontrado.")
        return []
    json_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.startswith("CyberMetric-") and f.endswith(".json")]
    json_files.sort()
    return json_files

def generate_output_path(root_dir: str, model_name: str, source_json_path: str, test_mode: str) -> str:
    """Gera o caminho completo para o ficheiro de resultados, mantendo a estrutura de pastas."""
    if ':' in model_name:
        model_family, model_params = model_name.split(':', 1)
    else:
        model_family, model_params = model_name, "latest"
    
    source_filename = os.path.basename(source_json_path)
    match = re.search(r'CyberMetric-(\d+)', source_filename)
    num_questions = match.group(1) if match else "unknown"
    
    name_stem = f"CyberMetric_{num_questions}_Results"
    if "_modified" in source_filename.lower(): name_stem += "_Modified"
    if test_mode == "Two-Step": name_stem += "_TwoStep"
    if test_mode == "Probabilistic": name_stem += "_Probabilistic"
        
    output_filename = f"{name_stem}.json"
    output_dir = os.path.join(root_dir, model_family, model_params)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, output_filename)

def load_cybermetric_tests(filename: str) -> List[Dict]:
    """Carrega as perguntas do ficheiro JSON, incluindo o texto da resposta correta."""
    try:
        with open(filename, 'r', encoding='utf-8') as f: data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return []
    
    test_cases = []
    questions_data = data.get("questions", [])
    for q_data in questions_data:
        question, answers, solution = q_data.get("question", ""), q_data.get("answers", {}), q_data.get("solution", "")
        if not all([question, answers, solution, solution in answers]): continue
        prompt_lines = [question] + [f"{key}) {value}" for key, value in sorted(answers.items())]
        test_cases.append({
            "category": f"CyberMetric-{len(questions_data)}", "question_only": question,
            "full_prompt": "\n".join(prompt_lines), "options_dict": answers,
            "expected_answer": solution.upper(), "expected_answer_text": answers[solution]
        })
    return test_cases

def extract_probabilities(response_text: str, options: list) -> tuple:
    """Motor de extração de probabilidades melhorado."""
    flags = {"parsing_failed": True, "summation_failed": False, "was_normalized": False}
    extracted = {}

    main_line_match = re.search(r"My confidence levels are:.*", response_text, re.IGNORECASE)
    search_area = main_line_match.group(0) if main_line_match else response_text
    
    for option in options:
        pattern = re.compile(rf'{option}\s*[:\-\(\s]*\s*(\d{{1,3}}(?:\.\d+)?)\s*%?')
        match = pattern.search(search_area)
        if match: extracted[option] = float(match.group(1))

    if not extracted: return {}, flags

    flags["parsing_failed"] = False

    for option in options:
        if option not in extracted: extracted[option] = 0.0

    total_prob = sum(extracted.values())

    if abs(total_prob - 100.0) > 1e-6:
        flags["summation_failed"] = True
        if total_prob > 0:
            factor = 100.0 / total_prob
            probabilities = {k: round(v * factor, 2) for k, v in extracted.items()}
            flags["was_normalized"] = True
        else:
            probabilities = extracted
    else:
        probabilities = {k: round(v, 2) for k, v in extracted.items()}

    return probabilities, flags

def save_results_to_json(results_data: Dict, output_filepath: str):
    """Guarda os resultados num ficheiro JSON no caminho especificado."""
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)
        print(f"\n[SUCCESS] Results file for analysis generated at: {output_filepath}")
    except IOError as e:
        print(f"[ERROR] Could not write results to JSON file '{output_filepath}': {e}")

# --- FUNÇÃO PRINCIPAL DO TESTADOR ---

def main():
    print("--- Cybersecurity Knowledge Tester (CyberMetric Edition) ---")

    mode_options = ["Standard Multiple-Choice Test", "Two-Step Reasoning Test", "Probabilistic Confidence Test"]
    selected_mode_str = beaupy.select(mode_options, cursor="> ", cursor_style="cyan")
    if not selected_mode_str: print("No test mode selected. Exiting."); return
    
    test_mode = "Standard"
    if "Two-Step" in selected_mode_str: test_mode = "Two-Step"
    if "Probabilistic" in selected_mode_str: test_mode = "Probabilistic"
    print(f"[INFO] Running in '{test_mode}' mode.")

    all_json_files = find_json_files(JSON_SOURCE_DIR)
    if not all_json_files: print("\nNo CyberMetric JSON files found. Exiting."); return
    
    files_to_test = []
    if beaupy.confirm(f"Found {len(all_json_files)} JSON files. Test all of them?", default_is_yes=False):
        files_to_test = all_json_files
    else:
        file_options = [os.path.basename(f) for f in all_json_files]
        selected_filename = beaupy.select(file_options, cursor="> ", cursor_style="cyan")
        if selected_filename: files_to_test.append(next(f for f in all_json_files if os.path.basename(f) == selected_filename))
    
    if not files_to_test: print("No JSON file selected. Exiting."); return

    available_models = list_ollama_models()
    if not available_models: return
    
    models_to_test = []
    if beaupy.confirm("Test ALL available models?", default_is_yes=False):
        models_to_test = available_models
    else:
        selected_model = beaupy.select(available_models, cursor="> ", cursor_style="cyan")
        if selected_model: models_to_test.append(selected_model)
    
    if not models_to_test: print("No model selected. Exiting."); return

    # --- CICLO PRINCIPAL DE EXECUÇÃO ---
    for json_filepath in files_to_test:
        test_cases = load_cybermetric_tests(json_filepath)
        if not test_cases:
            print(f"\nSkipping '{os.path.basename(json_filepath)}' as no test cases could be loaded.")
            continue
        
        print("\n" + "="*25 + f" STARTING FILE: {os.path.basename(json_filepath)} " + "="*25)

        for model_name in models_to_test:
            print(f"\n" + "#"*20 + f" TESTING MODEL: {model_name} ON {os.path.basename(json_filepath)} " + "#"*20)
            
            all_results_for_json = {"summary": {}, "details": {}}
            all_results_for_json["details"][model_name] = {}
            
            if test_mode == "Probabilistic":
                system_prompt = """You are an expert AI answering a multiple-choice cybersecurity question. Your task is to provide a probabilistic  score for each option and the sum of all percentages must equal 100%.

IMPORTANT: You must respond ONLY with a single line in the following format, and nothing else. Do not add explanations or any other text.

The format is: "My probabilities are: A: X%, B: Y%, C: Z%, ..."

Example response:
My probabilities are: A: 10%, B: 5%, C: 80%, D: 5%"""
                
                results_list = []
                summation_failures = 0
                for i, test_case in enumerate(test_cases):
                    print(f"\n--- Running Test {i+1}/{len(test_cases)} ---")
                    full_llm_response, _, duration = call_ollama(model_name, test_case['full_prompt'], system_prompt)
                    probabilities, flags = extract_probabilities(full_llm_response, list(test_case["options_dict"].keys()))
                    if flags["summation_failed"]: summation_failures += 1
                    
                    top_choice = max(probabilities, key=probabilities.get) if probabilities else None
                    is_correct = top_choice == test_case['expected_answer']
                    prob_for_correct = probabilities.get(test_case['expected_answer'], 0.0)

                    print(f"  -> Top Choice: '{top_choice}' | Correct: {is_correct} | Confidence in Correct Answer ({test_case['expected_answer']}): {prob_for_correct:.1f}%")

                    results_list.append({
                        "question_text": test_case['question_only'], "expected_answer_option": test_case['expected_answer'],
                        "expected_answer_text": test_case['expected_answer_text'], "llm_raw_response": full_llm_response,
                        "llm_extracted_probabilities": probabilities, "is_highest_prob_correct": is_correct,
                        "probability_assigned_to_correct_answer": prob_for_correct, "analysis_flags": flags
                    })
                
                total_tests = len(test_cases)
                confidences_on_correct = [r['probability_assigned_to_correct_answer'] for r in results_list]
                
                accuracy = sum(1 for r in results_list if r['is_highest_prob_correct']) / total_tests * 100 if total_tests > 0 else 0
                avg_conf = sum(confidences_on_correct) / total_tests if total_tests > 0 else 0
                
                conf_series = pd.Series(confidences_on_correct)
                median_conf = conf_series.median() if not conf_series.empty else 0
                variance_conf = conf_series.var(ddof=1) if len(conf_series) > 1 else 0  # variância amostral
                std_conf = conf_series.std(ddof=1) if len(conf_series) > 1 else 0       # desvio-padrão

                
                sum_fail_rate = summation_failures / total_tests * 100 if total_tests > 0 else 0

                all_results_for_json["summary"] = {
                    "accuracy_top_choice_percent": f"{accuracy:.2f}",
                    "average_confidence_on_correct_answer_percent": f"{avg_conf:.2f}",
                    "median_confidence_on_correct_answer_percent": f"{median_conf:.2f}",
                    "variance_of_confidence_on_correct_answer": f"{variance_conf:.2f}", # <<< NOVA MÉTRICA AQUI
                    "std_dev_of_confidence_on_correct_answer": f"{std_conf:.2f}",
                    "summation_failure_rate_percent": f"{sum_fail_rate:.2f}"
                }
                all_results_for_json["details"][model_name] = {f"Question_{i+1}": r for i, r in enumerate(results_list)}
                
                print(f"\n--- SUMMARY FOR MODEL: {model_name} ---")
                print(f"  Accuracy (Top Choice): {accuracy:.2f}%")
                print(f"  Avg. Confidence: {avg_conf:.2f}% | Median: {median_conf:.2f}% | Variance: {variance_conf:.2f} | Std Dev: {std_conf:.2f}")

                print(f"  Summation Fail Rate: {sum_fail_rate:.2f}%")

            elif test_mode == "Standard":
                system_prompt = "You are a cybersecurity expert taking a multiple-choice quiz. Please review the question and the options. Respond ONLY in this format (Answer: A, B, C, D, or E) with the letter of the correct option. You can provide a brief explanation before your final answer if necessary."
                correct_count = 0
                for i, test_case in enumerate(test_cases):
                    print(f"\n--- Running Test {i+1}/{len(test_cases)} ---")
                    full_llm_response, extracted_answer, duration = call_ollama(model_name, test_case['full_prompt'], system_prompt)
                    is_correct = (extracted_answer == test_case['expected_answer'])
                    if is_correct: correct_count += 1
                    print(f"Extracted Answer: '{extracted_answer}' | Expected: '{test_case['expected_answer']}' -> [ {'CORRECT' if is_correct else 'INCORRECT'} ] ({duration:.2f}s)")
                    all_results_for_json["details"][model_name][f"Question_{i+1}"] = {"question": test_case['question_only'], "full_llm_response": full_llm_response, "extracted_answer": extracted_answer, "expected_answer": test_case['expected_answer'], "is_correct": is_correct, "evaluation": "CORRECT" if is_correct else "INCORRECT", "response_time": f"{duration:.2f}"}
                total_tests = len(test_cases)
                accuracy = (correct_count / total_tests * 100) if total_tests > 0 else 0
                all_results_for_json["summary"] = {"correct": correct_count, "incorrect": total_tests - correct_count, "total": total_tests, "accuracy": f"{accuracy:.2f}%"}
                print(f"\n--- SUMMARY FOR MODEL: {model_name} ---")
                print(f"  Overall Accuracy: {accuracy:.2f}% ({correct_count} / {total_tests})")

            elif test_mode == "Two-Step":
                system_prompt_step1 = "You are a cybersecurity expert. Answer the following question directly and concisely based on your knowledge. Do not mention or guess any multiple-choice options."
                system_prompt_step2 = "Your task is to compare your previous answer with a list of options. Based *exclusively* on your previous answer provided in the context below, choose the option that best represents it."
                option_correct_count = 0
                for i, test_case in enumerate(test_cases):
                    print(f"\n--- Running Test {i+1}/{len(test_cases)} ---")
                    print("  Step 1: Generating free-text response...")
                    step1_response, _, duration1 = call_ollama(model_name, test_case['question_only'], system_prompt_step1)
                    print("  Step 2: Mapping response to options...")
                    prompt_step2 = f"[START OF YOUR PREVIOUS RESPONSE]\n\n{step1_response}\n\n[END OF YOUR PREVIOUS RESPONSE]\n\nOriginal Question: {test_case['question_only']}\n\nBased only on your previous response provided above, which of the following options (A, B, C, D, E) is the closest match?\n\n{test_case['full_prompt'].replace(test_case['question_only'], '')}\n\nRespond ONLY in this format (Answer: A, B, C, D, or E) with the letter of the correct option. You can provide a brief explanation before your final answer if necessary."
                    _, step2_selected_option, duration2 = call_ollama(model_name, prompt_step2, system_prompt_step2)
                    is_option_correct = (step2_selected_option == test_case['expected_answer'])
                    if is_option_correct: option_correct_count += 1
                    print(f"  -> Selected Option: '{step2_selected_option}' | Expected: '{test_case['expected_answer']}' -> [ {'OPTION CORRECT' if is_option_correct else 'OPTION INCORRECT'} ] (Total time: {duration1+duration2:.2f}s)")
                    all_results_for_json["details"][model_name][f"Question_{i+1}"] = {"question_text": test_case['question_only'], "expected_option": test_case['expected_answer'],"step1_free_response": step1_response, "step2_selected_option": step2_selected_option, "is_option_correct": is_option_correct, "manual_overall_evaluation": ""}
                total_tests = len(test_cases)
                option_accuracy = (option_correct_count / total_tests * 100) if total_tests > 0 else 0
                all_results_for_json["summary"] = {"provisory_option_correct": option_correct_count, "provisory_option_incorrect": total_tests - option_correct_count, "total": total_tests, "option_mapping_accuracy": f"{option_accuracy:.2f}%"}
                print(f"\n--- PROVISORY SUMMARY FOR MODEL: {model_name} ---")
                print(f"  Option Mapping Accuracy: {option_accuracy:.2f}% ({option_correct_count} / {total_tests} correct option choices)")

            # --- Guardar os Resultados ---
            output_filepath = generate_output_path(RESULTS_ROOT_DIR, model_name, json_filepath, test_mode)
            save_results_to_json(all_results_for_json, output_filepath)

    print("\n--- All selected tests are complete. ---")

if __name__ == "__main__":
    main()