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
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# O ficheiro de entrada com os cenários de modelação de ameaças
THREAT_MODEL_TESTS_FILE = os.path.join(SCRIPT_DIR, "ThreatModel_Tests.json")
RESULTS_ROOT_DIR = os.path.join(SCRIPT_DIR, "ResultsThreatModeling")

OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_TAGS_ENDPOINT_SUFFIX = "/tags"
OLLAMA_GENERATE_ENDPOINT_SUFFIX = "/generate"
OLLAMA_REQUEST_TIMEOUT_SECONDS = 700
OLLAMA_KEEP_ALIVE_DURATION = "5m"

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

def call_ollama_for_text(model_name: str, user_prompt: str, system_prompt: str) -> Tuple[str, float]:
    """Chama a API Ollama e retorna a resposta de texto completa e a duração."""
    payload = {"model": model_name, "system": system_prompt, "prompt": user_prompt, "stream": False, "keep_alive": OLLAMA_KEEP_ALIVE_DURATION}
    start_time = time.perf_counter()
    try:
        response = requests.post(f"{OLLAMA_API_BASE_URL}{OLLAMA_GENERATE_ENDPOINT_SUFFIX}", json=payload, timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        response_data = response.json()
        duration = time.perf_counter() - start_time
        full_response = response_data.get("response", "Error: No 'response' key in Ollama's output.").strip()
        return full_response, duration
    except Exception as e:
        duration = time.perf_counter() - start_time
        error_msg = f"Error: Request to Ollama failed: {e}"
        return error_msg, duration

def load_threat_model_tests(filename: str) -> List[Dict]:
    """Carrega os cenários de modelação de ameaças do ficheiro JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"[ERROR] O ficheiro de teste '{filename}' não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] O ficheiro '{filename}' não é um JSON válido.")
        return []

def generate_output_path(root_dir: str, model_name: str) -> str:
    """Gera o caminho de saída para o ficheiro de resultados de modelação de ameaças."""
    if ':' in model_name:
        model_family, model_params = model_name.split(':', 1)
    else:
        model_family, model_params = model_name, "latest"
    
    output_filename = "ThreatModel_Results.json" # Nome de ficheiro fixo para este tipo de teste
    output_dir = os.path.join(root_dir, model_family, model_params)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, output_filename)

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
    print("--- Qualitative Threat Modeling Tester ---")

    threat_model_tests = load_threat_model_tests(THREAT_MODEL_TESTS_FILE)
    if not threat_model_tests:
        print("No test cases could be loaded. Exiting.")
        return
    print(f"[INFO] Loaded {len(threat_model_tests)} threat modeling scenarios.")

    available_models = list_ollama_models()
    if not available_models: return
    
    models_to_test = []
    if beaupy.confirm("Test ALL available models?", default_is_yes=False):
        models_to_test = available_models
    else:
        selected_model = beaupy.select(available_models, cursor="> ", cursor_style="cyan")
        if selected_model: models_to_test.append(selected_model)
    
    if not models_to_test:
        print("No model selected. Exiting.")
        return

    system_prompt = "You are a senior cybersecurity threat modeling expert. Your task is to analyze the provided system architecture and answer the specific questions that follow. Be precise, structured, and base your answers only on the provided context."

    for model_name in models_to_test:
        print("\n" + "#"*20 + f" TESTING MODEL: {model_name} " + "#"*20)
        
        qualitative_results = {
            "model_name": model_name,
            "test_date": datetime.datetime.now().isoformat(),
            "results": {}
        }

        for i, test_case in enumerate(threat_model_tests):
            test_id = test_case['test_id']
            print(f"\n--- Running Scenario {i+1}/{len(threat_model_tests)}: [{test_id}] {test_case['title']} ---")

            model_responses = {}
            
            # --- Pergunta Sequencial 1: Identificar Ameaças ---
            q1 = test_case["questions"][0]
            print(f"  -> Asking: {q1['prompt']}")
            prompt1 = f"Architecture Description:\n---\n{test_case['architecture_description']}\n---\n\nQuestion: {q1['prompt']}"
            response1, duration1 = call_ollama_for_text(model_name, prompt1, system_prompt)
            model_responses[q1['q_id']] = response1
            
            time.sleep(1) # Pequena pausa entre chamadas

            # --- Pergunta Sequencial 2: Propor Mitigações ---
            q2 = test_case["questions"][1]
            print(f"  -> Asking: {q2['prompt']}")
            prompt2 = f"""Here is the original architecture description:
---
{test_case['architecture_description']}
---
Previously, you were asked: '{q1['prompt']}'
Your response was:
---
{response1}
---
Now, based on that context, answer the following question: {q2['prompt']}"""
            response2, duration2 = call_ollama_for_text(model_name, prompt2, system_prompt)
            model_responses[q2['q_id']] = response2

            # --- Estruturar o resultado para este cenário ---
            qualitative_results["results"][test_id] = {
                "title": test_case["title"],
                "domain": test_case["domain"],
                "architecture_description": test_case["architecture_description"],
                "model_responses": model_responses,
                "evaluation_rubric": test_case["evaluation_rubric"], # Incluir a chave de resposta
                "manual_evaluation": { # Deixar em branco para preenchimento
                    "threat_identification_score_1_to_5": None,
                    "mitigation_quality_score_1_to_5": None,
                    "structured_reasoning_score_1_to_5": None,
                    "notes": ""
                }
            }
            print(f"  -> Scenario '{test_id}' completed in {duration1+duration2:.2f}s.")

        # --- Guardar o ficheiro de resultados completo para este modelo ---
        output_filepath = generate_output_path(RESULTS_ROOT_DIR, model_name)
        save_results_to_json(qualitative_results, output_filepath)

    print("\n--- All qualitative tests are complete. ---")

if __name__ == "__main__":
    main()