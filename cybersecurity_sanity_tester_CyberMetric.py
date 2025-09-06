# cybermetric_tester.py

import os
import datetime
import re
import time
import json
import beaupy
from typing import List, Dict, Optional, Any, Tuple

# --- DEPENDÊNCIAS ---
# pip install requests beaupy
import requests

# --- CONFIGURAÇÕES ---

OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_TAGS_ENDPOINT_SUFFIX = "/tags"
OLLAMA_GENERATE_ENDPOINT_SUFFIX = "/generate"
OLLAMA_REQUEST_TIMEOUT_SECONDS = 700
OLLAMA_KEEP_ALIVE_DURATION = "5m"

LOG_DIR_NAME = "cybersecurity_test_logs"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_JSON_FILENAME = "CyberMetric_Results.json"
CYBERMETRIC_JSON_FILENAME = "CyberMetric-7.json" # Nome do ficheiro com as perguntas

# --- MÓDULOS OLLAMA E LOGGING ---

def list_ollama_models() -> List[str]:
    try:
        response = requests.get(f"{OLLAMA_API_BASE_URL}{OLLAMA_TAGS_ENDPOINT_SUFFIX}", timeout=10)
        response.raise_for_status()
        models = [model["name"] for model in response.json().get("models", [])]
        if not models: raise ValueError("No models found")
        models.sort()
        return models
    except Exception as e:
        print(f"[ERROR] Could not fetch models from Ollama: {e}")
        print("  Please ensure Ollama is running and accessible.")
        return []

def call_ollama(model_name: str, user_prompt: str, system_prompt: str) -> Tuple[str, Optional[str], float]:
    """
    Chama a API Ollama e processa a resposta de forma inteligente.
    
    Retorna uma tupla com:
    - A resposta completa e original do LLM (para logging).
    - A letra da resposta extraída (A, B, C, ou D) para verificação.
    - A duração da chamada.
    """
    payload = { "model": model_name, "system": system_prompt, "prompt": user_prompt, "stream": False, "keep_alive": OLLAMA_KEEP_ALIVE_DURATION }
    start_time = time.perf_counter()
    try:
        response = requests.post(f"{OLLAMA_API_BASE_URL}{OLLAMA_GENERATE_ENDPOINT_SUFFIX}", json=payload, timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        response_data = response.json()
        duration = time.perf_counter() - start_time
        
        full_response = response_data.get("response", "Error: No 'response' key in Ollama's output.").strip()
        
        # <<< NOVA LÓGICA DE EXTRAÇÃO INTELIGENTE >>>
        extracted_answer = None

        # Estratégia 1: Procurar por um padrão forte como "Answer: B"
        strong_pattern_match = re.search(r'(?:answer is|answer:)\s*\**\s*\b([A-D])\b', full_response, re.IGNORECASE)
        if strong_pattern_match:
            extracted_answer = strong_pattern_match.group(1).upper()
        else:
            # Estratégia 2 (Fallback): Procurar a última letra solta (A-D) na resposta
            all_standalone_letters = re.findall(r'\b([A-D])\b', full_response, re.IGNORECASE)
            if all_standalone_letters:
                extracted_answer = all_standalone_letters[-1].upper()
            else:
                # Se nenhuma estratégia funcionar, a resposta é considerada inanalisável
                extracted_answer = full_response

        return full_response, extracted_answer, duration

    except requests.exceptions.RequestException as e:
        duration = time.perf_counter() - start_time
        error_msg = f"Error: Request to Ollama failed: {e}"
        return error_msg, error_msg, duration
    except Exception as e:
        duration = time.perf_counter() - start_time
        error_msg = f"Error: An unexpected error occurred: {e}"
        return error_msg, error_msg, duration

class TestLogger:
    def __init__(self):
        self.log_filepath: Optional[str] = None
        self.model_timings: Dict[str, List[float]] = {}
    def initialize(self, run_mode_key: str):
        log_dir = os.path.join(SCRIPT_DIR, LOG_DIR_NAME)
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filepath = os.path.join(log_dir, f"test_run_{run_mode_key}_{timestamp}.txt")
        header = f"Cybersecurity Sanity Test Log\nRun Mode: {run_mode_key}\nInitialized: {datetime.datetime.now().isoformat()}\n" + "="*50 + "\n\n"
        try:
            with open(self.log_filepath, 'w', encoding='utf-8') as f: f.write(header)
            print(f"[INFO] Log file initialized at: {self.log_filepath}")
        except IOError as e:
            print(f"[ERROR] Could not create log file: {e}")
            self.log_filepath = None
    def log_test_case(self, model_name: str, test_case: Dict[str, Any], system_prompt: str, full_llm_response: str, duration: float):
        if not self.log_filepath: return
        if model_name not in self.model_timings: self.model_timings[model_name] = []
        self.model_timings[model_name].append(duration)
        log_entry = [
            f"--- Test Case Start ---",
            f"Timestamp: {datetime.datetime.now().isoformat()}",
            f"Model: {model_name}",
            f"Category: {test_case['category']}",
            f"Response Time: {duration:.2f} seconds",
            f"\nSYSTEM PROMPT:\n{system_prompt}",
            f"\nUSER PROMPT:\n{test_case['prompt']}",
            f"\n--- FULL LLM RESPONSE (for logging) ---\n{full_llm_response}",
            f"\n--- EXPECTED ANSWER --- \n{test_case['expected_answer']}",
            f"\n--- End of Test Case ---\n" + "="*50 + "\n\n"
        ]
        try:
            with open(self.log_filepath, 'a', encoding='utf-8') as f: f.write("\n".join(log_entry))
        except IOError as e: print(f"[ERROR] Could not write to log file: {e}")
    def log_summary(self, models_tested: List[str], num_tests: int, results_summary: Dict):
        if not self.log_filepath: return
        summary = ["--- Run Summary ---"]
        for model_name in models_tested:
            timings = self.model_timings.get(model_name, [])
            stats = results_summary.get(model_name, {})
            if timings:
                avg_time = sum(timings) / len(timings)
                total_time = sum(timings)
                summary.append(f"\nModel: {model_name}\n  - Total Tests: {len(timings)}\n  - Correct Answers: {stats.get('correct', 0)}\n  - Incorrect Answers: {stats.get('incorrect', 0)}\n  - Accuracy: {stats.get('accuracy', 'N/A')}\n  - Total Time Spent in LLM Calls: {total_time:.2f} seconds\n  - Average Response Time: {avg_time:.2f} seconds")
        summary.append(f"\nTotal Number of Test Cases Configured: {num_tests}")
        summary.append(f"\nEnd of Log.")
        try:
            with open(self.log_filepath, 'a', encoding='utf-8') as f: f.write("\n".join(summary))
        except IOError as e: print(f"[ERROR] Could not write summary to log file: {e}")

def save_results_to_json(results_data: Dict, output_filename: str):
    filepath = os.path.join(SCRIPT_DIR, output_filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=4)
        print(f"\n[SUCCESS] Results file for analysis generated at: {filepath}")
    except IOError as e:
        print(f"[ERROR] Could not write results to JSON file '{filepath}': {e}")

def load_cybermetric_tests(filename: str) -> List[Dict]:
    filepath = os.path.join(SCRIPT_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f: data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] The file '{filename}' was not found in the script directory.")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] The file '{filename}' is not a valid JSON file.")
        return []
    test_cases = []
    for q_data in data.get("questions", []):
        question, answers, solution = q_data.get("question", ""), q_data.get("answers", {}), q_data.get("solution", "")
        if not all([question, answers, solution, solution in answers]): continue
        prompt_lines = [question] + [f"{key}) {value}" for key, value in sorted(answers.items())]
        test_cases.append({
            "category": "CyberMetric Quiz",
            "prompt": "\n".join(prompt_lines),
            "expected_answer": solution.upper(),
            "full_correct_answer_text": answers[solution]
        })
    return test_cases

# --- FUNÇÃO PRINCIPAL DO TESTADOR ---

def main():
    print("--- Cybersecurity Knowledge Sanity Tester (CyberMetric Edition) ---")
    
    TEST_CASES = load_cybermetric_tests(CYBERMETRIC_JSON_FILENAME)
    if not TEST_CASES:
        print("\nNo test cases could be loaded. Exiting.")
        return
    print(f"[INFO] Loaded {len(TEST_CASES)} test cases from '{CYBERMETRIC_JSON_FILENAME}'.")

    available_models = list_ollama_models()
    if not available_models: return

    run_all = beaupy.confirm("Do you want to test ALL available models?", default_is_yes=False)
    
    models_to_test = available_models if run_all else ([beaupy.select(available_models, cursor="> ", cursor_style="cyan")] if beaupy.select else [])
    if not models_to_test or not models_to_test[0]:
        print("No model selected. Exiting.")
        return
    if run_all: print(f"[INFO] Selected all {len(models_to_test)} models for testing.")

    run_mode_key = "all_models_cybermetric" if run_all else re.sub(r'[^a-zA-Z0-9]', '_', models_to_test[0])
    logger = TestLogger()
    logger.initialize(run_mode_key)

    system_prompt_for_tests = "You are a cybersecurity expert taking a multiple-choice quiz. Please review the question and the options. Respond ONLY in this format (Answer: A, B, C, or D) with the letter of the correct option. You can provide a brief explanation before your final answer if necessary."

    all_results_for_json = {"summary": {}, "details": {}}
    run_summary = {}

    for model_name in models_to_test:
        print(f"\n" + "#"*20 + f" TESTING MODEL: {model_name} " + "#"*20)
        all_results_for_json["details"][model_name] = {}
        correct_count = 0
        
        for i, test_case in enumerate(TEST_CASES):
            print(f"\n--- Running Test {i+1}/{len(TEST_CASES)}: [{test_case['category']}] ---")
            print(f"  Question > {test_case['prompt'].splitlines()[0]}")

            full_llm_response, extracted_answer, duration = call_ollama(model_name, test_case['prompt'], system_prompt_for_tests)
            
            is_correct = (extracted_answer == test_case['expected_answer'])
            result_str = "CORRECT" if is_correct else "INCORRECT"
            if is_correct: correct_count += 1

            # <<< ALTERAÇÃO: Apresentação limpa no terminal >>>
            print(f"\nExtracted Answer: '{extracted_answer}' | Expected: '{test_case['expected_answer']}' -> [ {result_str} ]")
            print(f"(Response time: {duration:.2f} seconds)")
            
            # Informa o utilizador que a resposta completa foi logada, se for diferente
            if extracted_answer != full_llm_response and len(full_llm_response) > 50:
                print(f"  (Full response including reasoning was saved to the log file)")

            logger.log_test_case(model_name, test_case, system_prompt_for_tests, full_llm_response, duration)
            
            all_results_for_json["details"][model_name][f"Question_{i+1}"] = {
                "question": test_case['prompt'].splitlines()[0],
                "full_prompt": test_case['prompt'],
                "full_llm_response": full_llm_response,
                "extracted_answer": extracted_answer,
                "expected_answer": test_case['expected_answer'],
                "is_correct": is_correct,
                "evaluation": result_str,
                "response_time": f"{duration:.2f}"
            }
            
            if not is_correct:
                print(f"  > The correct answer is {test_case['expected_answer']}: {test_case['full_correct_answer_text']}")
            print("\n" + "*"*60)

        # (Sem alterações nesta secção de resumo)
        total_tests = len(TEST_CASES)
        accuracy = (correct_count / total_tests * 100) if total_tests > 0 else 0
        run_summary[model_name] = {
            "correct": correct_count,
            "incorrect": total_tests - correct_count,
            "total": total_tests,
            "accuracy": f"{accuracy:.2f}%"
        }
        print(f"\n--- SUMMARY FOR MODEL: {model_name} ---")
        print(f"  Correct Answers: {correct_count} / {total_tests}")
        print(f"  Accuracy: {accuracy:.2f}%")
        print("-" * (25 + len(model_name)))

    all_results_for_json["summary"] = run_summary
    logger.log_summary(models_to_test, len(TEST_CASES), run_summary)
    save_results_to_json(all_results_for_json, RESULTS_JSON_FILENAME)
    
    print("\n--- Testing complete. Check log file for a full record. ---")
    print(f"--- A '{RESULTS_JSON_FILENAME}' file has been created with detailed results and a final summary. ---")

if __name__ == "__main__":
    main()