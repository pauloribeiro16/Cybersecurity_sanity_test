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

# <<< ALTERAÇÃO: Configurações de diretórios >>>
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Diretório onde os ficheiros CyberMetric-*.json estão guardados
JSON_SOURCE_DIR = os.path.join(SCRIPT_DIR, "Json_CyberMetrics")
# Diretório raiz onde todos os resultados serão guardados
RESULTS_ROOT_DIR = os.path.join(SCRIPT_DIR, "ResultsCyberMetrics")

OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_TAGS_ENDPOINT_SUFFIX = "/tags"
OLLAMA_GENERATE_ENDPOINT_SUFFIX = "/generate"
OLLAMA_REQUEST_TIMEOUT_SECONDS = 700
OLLAMA_KEEP_ALIVE_DURATION = "5m"

LOG_DIR_NAME = "cybersecurity_test_logs"


# --- FUNÇÕES AUXILIARES ---

# <<< NOVO: Função para encontrar ficheiros de teste JSON >>>
def find_json_files(source_dir: str) -> List[str]:
    """Procura por ficheiros .json num diretório e retorna os seus caminhos completos."""
    if not os.path.isdir(source_dir):
        print(f"[ERROR] O diretório de origem '{source_dir}' não foi encontrado.")
        return []
    
    json_files = [
        os.path.join(source_dir, f) 
        for f in os.listdir(source_dir) 
        if f.startswith("CyberMetric-") and f.endswith(".json")
    ]
    json_files.sort()
    return json_files

# <<< NOVO: Função para criar a estrutura de pastas e nome do ficheiro de saída >>>
def generate_output_path(root_dir: str, model_name: str, source_json_path: str) -> str:
    """
    Gera o caminho completo para o ficheiro de resultados, criando as pastas necessárias.
    Exemplo: ResultsCyberMetrics/qwen3/8b/CyberMetric_80_Results.json
    """
    # 1. Analisar o nome do modelo
    if ':' in model_name:
        model_family, model_params = model_name.split(':', 1)
    else:
        model_family, model_params = model_name, "latest"
    
    # 2. Analisar o nome do ficheiro de origem para extrair o número
    source_filename = os.path.basename(source_json_path)
    match = re.search(r'CyberMetric-(\d+)-v\d+\.json', source_filename)
    num_questions = match.group(1) if match else "unknown"
    
    # 3. Construir o nome do ficheiro de destino
    output_filename = f"CyberMetric_{num_questions}_Results.json"
    
    # 4. Construir o caminho completo do diretório
    output_dir = os.path.join(root_dir, model_family, model_params)
    
    # 5. Criar os diretórios se não existirem
    os.makedirs(output_dir, exist_ok=True)
    
    # 6. Retornar o caminho completo do ficheiro
    return os.path.join(output_dir, output_filename)

def load_cybermetric_tests(filename: str) -> List[Dict]:
    """Carrega as perguntas do ficheiro JSON especificado."""
    # (Lógica interna da função permanece a mesma)
    try:
        with open(filename, 'r', encoding='utf-8') as f: data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] The file '{filename}' was not found.")
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
            "category": f"CyberMetric-{len(data.get('questions', []))}",
            "prompt": "\n".join(prompt_lines),
            "expected_answer": solution.upper(),
            "full_correct_answer_text": answers[solution]
        })
    return test_cases

# --- MÓDULOS OLLAMA E LOGGING (sem alterações) ---
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
        return []

def call_ollama(model_name: str, user_prompt: str, system_prompt: str) -> Tuple[str, Optional[str], float]:
    payload = { "model": model_name, "system": system_prompt, "prompt": user_prompt, "stream": False, "keep_alive": OLLAMA_KEEP_ALIVE_DURATION }
    start_time = time.perf_counter()
    try:
        response = requests.post(f"{OLLAMA_API_BASE_URL}{OLLAMA_GENERATE_ENDPOINT_SUFFIX}", json=payload, timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        response_data = response.json()
        duration = time.perf_counter() - start_time
        full_response = response_data.get("response", "Error: No 'response' key in Ollama's output.").strip()
        strong_pattern_match = re.search(r'(?:answer is|answer:)\s*\**\s*\b([A-D])\b', full_response, re.IGNORECASE)
        if strong_pattern_match:
            extracted_answer = strong_pattern_match.group(1).upper()
        else:
            all_standalone_letters = re.findall(r'\b([A-D])\b', full_response, re.IGNORECASE)
            extracted_answer = all_standalone_letters[-1].upper() if all_standalone_letters else full_response
        return full_response, extracted_answer, duration
    except Exception as e:
        duration = time.perf_counter() - start_time
        error_msg = f"Error: Request to Ollama failed: {e}"
        return error_msg, error_msg, duration

class TestLogger: # (sem alterações na classe Logger)
    def __init__(self): self.log_filepath: Optional[str] = None; self.model_timings: Dict[str, List[float]] = {}
    def initialize(self, run_mode_key: str): # ... (código igual)
        log_dir=os.path.join(SCRIPT_DIR,LOG_DIR_NAME); os.makedirs(log_dir,exist_ok=True); timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); self.log_filepath=os.path.join(log_dir,f"test_run_{run_mode_key}_{timestamp}.txt"); header=f"Cybersecurity Sanity Test Log\nRun Mode: {run_mode_key}\nInitialized: {datetime.datetime.now().isoformat()}\n" + "="*50 + "\n\n";
        try:
            with open(self.log_filepath,'w',encoding='utf-8') as f: f.write(header); print(f"[INFO] Log file initialized at: {self.log_filepath}")
        except IOError as e: print(f"[ERROR] Could not create log file: {e}"); self.log_filepath=None
    def log_test_case(self, model_name: str, test_case: Dict[str, Any], system_prompt: str, full_llm_response: str, duration: float): # ... (código igual)
        if not self.log_filepath: return
        if model_name not in self.model_timings: self.model_timings[model_name]=[]
        self.model_timings[model_name].append(duration); log_entry=[f"--- Test Case Start ---",f"Timestamp: {datetime.datetime.now().isoformat()}",f"Model: {model_name}",f"Category: {test_case['category']}",f"Response Time: {duration:.2f} seconds",f"\nSYSTEM PROMPT:\n{system_prompt}",f"\nUSER PROMPT:\n{test_case['prompt']}",f"\n--- FULL LLM RESPONSE (for logging) ---\n{full_llm_response}",f"\n--- EXPECTED ANSWER --- \n{test_case['expected_answer']}",f"\n--- End of Test Case ---\n" + "="*50 + "\n\n"];
        try:
            with open(self.log_filepath,'a',encoding='utf-8') as f: f.write("\n".join(log_entry))
        except IOError as e: print(f"[ERROR] Could not write to log file: {e}")
    def log_summary(self, models_tested: List[str], num_tests: int, results_summary: Dict): # ... (código igual)
        if not self.log_filepath: return
        summary=["--- Run Summary ---"];
        for model_name in models_tested:
            timings=self.model_timings.get(model_name,[]); stats=results_summary.get(model_name,{});
            if timings:
                avg_time=sum(timings)/len(timings); total_time=sum(timings); summary.append(f"\nModel: {model_name}\n  - Total Tests: {len(timings)}\n  - Correct Answers: {stats.get('correct',0)}\n  - Incorrect Answers: {stats.get('incorrect',0)}\n  - Accuracy: {stats.get('accuracy','N/A')}\n  - Total Time Spent in LLM Calls: {total_time:.2f} seconds\n  - Average Response Time: {avg_time:.2f} seconds")
        summary.append(f"\nTotal Number of Test Cases Configured: {num_tests}"); summary.append(f"\nEnd of Log.");
        try:
            with open(self.log_filepath,'a',encoding='utf-8') as f: f.write("\n".join(summary))
        except IOError as e: print(f"[ERROR] Could not write summary to log file: {e}")

# <<< ALTERAÇÃO: A função agora aceita um caminho completo para o ficheiro >>>
def save_results_to_json(results_data: Dict, output_filepath: str):
    """Guarda os resultados num ficheiro JSON no caminho especificado."""
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=4)
        print(f"\n[SUCCESS] Results file for analysis generated at: {output_filepath}")
    except IOError as e:
        print(f"[ERROR] Could not write results to JSON file '{output_filepath}': {e}")


# --- FUNÇÃO PRINCIPAL DO TESTADOR ---

def main():
    print("--- Cybersecurity Knowledge Sanity Tester (CyberMetric Edition) ---")
    
    # <<< ALTERAÇÃO: Lógica de seleção de ficheiros JSON >>>
    all_json_files = find_json_files(JSON_SOURCE_DIR)
    if not all_json_files:
        print("\nNo CyberMetric JSON files found. Exiting.")
        return
    
    files_to_test = []
    test_all_files = beaupy.confirm(f"Found {len(all_json_files)} JSON files. Do you want to test ALL of them?", default_is_yes=False)
    if test_all_files:
        files_to_test = all_json_files
        print(f"[INFO] Selected all {len(files_to_test)} JSON files for testing.")
    else:
        # Apresentar nomes de ficheiros em vez de caminhos completos
        file_options = [os.path.basename(f) for f in all_json_files]
        selected_filename = beaupy.select(file_options, cursor="> ", cursor_style="cyan")
        if selected_filename:
            # Encontrar o caminho completo correspondente ao nome do ficheiro selecionado
            files_to_test.append(next(f for f in all_json_files if os.path.basename(f) == selected_filename))
    
    if not files_to_test:
        print("No JSON file selected. Exiting.")
        return

    # <<< ALTERAÇÃO: Lógica de seleção de modelos (permanece igual, mas a sua posição é importante) >>>
    available_models = list_ollama_models()
    if not available_models: return

    run_all_models = beaupy.confirm("Do you want to test ALL available models?", default_is_yes=False)
    models_to_test = []
    if run_all_models:
        models_to_test = available_models
        print(f"[INFO] Selected all {len(models_to_test)} models for testing.")
    else:
        selected_model = beaupy.select(available_models, cursor="> ", cursor_style="cyan")
        if selected_model:
            models_to_test.append(selected_model)
    
    if not models_to_test:
        print("No model selected. Exiting.")
        return

    # <<< ALTERAÇÃO: O logger é inicializado uma vez para a execução completa >>>
    logger = TestLogger()
    logger.initialize("CyberMetric_Multi_Run")
    
    system_prompt_for_tests = "You are a cybersecurity expert taking a multiple-choice quiz. Please review the question and the options. Respond ONLY in this format (Answer: A, B, C, or D) with the letter of the correct option. You can provide a brief explanation before your final answer if necessary."

    # <<< ALTERAÇÃO: Ciclo principal duplo (ficheiros -> modelos) >>>
    for json_filepath in files_to_test:
        test_cases = load_cybermetric_tests(json_filepath)
        if not test_cases:
            print(f"\nSkipping '{os.path.basename(json_filepath)}' as no test cases could be loaded.")
            continue
        
        print("\n" + "="*25 + f" STARTING FILE: {os.path.basename(json_filepath)} " + "="*25)
        print(f"[INFO] Loaded {len(test_cases)} test cases.")

        for model_name in models_to_test:
            print(f"\n" + "#"*20 + f" TESTING MODEL: {model_name} ON {os.path.basename(json_filepath)} " + "#"*20)
            
            all_results_for_json = {"summary": {}, "details": {}}
            run_summary = {}
            all_results_for_json["details"][model_name] = {}
            correct_count = 0
            
            for i, test_case in enumerate(test_cases):
                print(f"\n--- Running Test {i+1}/{len(test_cases)} ---")
                
                full_llm_response, extracted_answer, duration = call_ollama(model_name, test_case['prompt'], system_prompt_for_tests)
                
                is_correct = (extracted_answer == test_case['expected_answer'])
                result_str = "CORRECT" if is_correct else "INCORRECT"
                if is_correct: correct_count += 1

                print(f"Extracted Answer: '{extracted_answer}' | Expected: '{test_case['expected_answer']}' -> [ {result_str} ] ({duration:.2f}s)")
                
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
            
            # Resumo para esta combinação de modelo e ficheiro
            total_tests = len(test_cases)
            accuracy = (correct_count / total_tests * 100) if total_tests > 0 else 0
            run_summary[model_name] = {
                "correct": correct_count, "incorrect": total_tests - correct_count,
                "total": total_tests, "accuracy": f"{accuracy:.2f}%"
            }
            print(f"\n--- SUMMARY FOR MODEL: {model_name} ---")
            print(f"  Correct Answers: {correct_count} / {total_tests} | Accuracy: {accuracy:.2f}%")
            
            # Guardar os resultados
            all_results_for_json["summary"] = run_summary
            # <<< ALTERAÇÃO: Gerar caminho de saída e guardar ficheiro >>>
            output_filepath = generate_output_path(RESULTS_ROOT_DIR, model_name, json_filepath)
            save_results_to_json(all_results_for_json, output_filepath)

    print("\n--- All selected tests are complete. Check the log file and the 'ResultsCyberMetrics' directory. ---")

if __name__ == "__main__":
    main()