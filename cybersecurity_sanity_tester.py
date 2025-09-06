# cybersecurity_sanity_tester.py

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
RESULTS_JSON_FILENAME = "Results.json"


# --- CASOS DE TESTE INICIAIS ---
# (Sem alterações aqui)
TEST_CASES = [
    {
        "category": "Basic Definitions",
        "prompt": "What is a security requirement?",
        "expected_short_answer": "A security requirement is a statement of needed security functionality or a constraint that ensures the security of a system or application.",
        "expected_keywords": ["statement", "constraint", "functionality", "security"],
        "source_url": "https://csrc.nist.gov/glossary/term/security_requirement"
    },
    {
        "category": "Frameworks",
        "prompt": "What are the five core functions of the NIST Cybersecurity Framework (CSF)?",
        "expected_short_answer": "The five core functions of the NIST CSF are Identify, Protect, Detect, Respond, and Recover.",
        "expected_keywords": ["identify", "protect", "detect", "respond", "recover"],
        "source_url": "https://www.nist.gov/cyberframework/framework"
    },
    {
        "category": "Security Controls",
        "prompt": "Which NIST 800-53 control family is primarily responsible for audit and accountability?",
        "expected_short_answer": "The 'AU' (Audit and Accountability) control family is responsible for audit logging and related controls.",
        "expected_keywords": ["au", "audit", "accountability"],
        "source_url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final"
    },
    {
        "category": "Vulnerabilities",
        "prompt": "What is CWE-79 and what type of vulnerability does it represent?",
        "expected_short_answer": "CWE-79 is 'Improper Neutralization of Input During Web Page Generation', commonly known as Cross-Site Scripting (XSS). It's an injection vulnerability.",
        "expected_keywords": ["cwe-79", "cross-site scripting", "xss", "injection", "neutralization"],
        "source_url": "https://cwe.mitre.org/data/definitions/79.html"
    },
    {
        "category": "Threat Modeling",
        "prompt": "What does STRIDE stand for in threat modeling?",
        "expected_short_answer": "STRIDE stands for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.",
        "expected_keywords": ["spoofing", "tampering", "repudiation", "information disclosure", "denial of service", "elevation of privilege"],
        "source_url": "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats"
    },
    {
        "category": "Regulations/Directives",
        "prompt": "What is the main difference between NIS 2 Directive and GDPR?",
        "expected_short_answer": "GDPR protects personal data across all sectors, while the NIS 2 Directive focuses on the operational cybersecurity and resilience of critical infrastructure and essential services.",
        "expected_keywords": ["personal data", "gdpr", "nis 2", "cybersecurity", "resilience", "critical infrastructure"],
        "source_url": "https://www.enisa.europa.eu/topics/nis-directive"
    },
    {
        "category": "Basic Principles",
        "prompt": "What does the CIA triad stand for in information security?",
        "expected_short_answer": "The CIA triad stands for Confidentiality, Integrity, and Availability.",
        "expected_keywords": ["confidentiality", "integrity", "availability"],
        "source_url": "https://csrc.nist.gov/glossary/term/confidentiality"
    }
]



# --- MÓDULOS OLLAMA E LOGGING ---
# (Sem alterações nestas secções, mantêm-se como na resposta anterior)
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

def call_ollama(model_name: str, user_prompt: str, system_prompt: str) -> Tuple[str, float]:
    payload = { "model": model_name, "system": system_prompt, "prompt": user_prompt, "stream": False, "keep_alive": OLLAMA_KEEP_ALIVE_DURATION }
    start_time = time.perf_counter()
    try:
        response = requests.post(f"{OLLAMA_API_BASE_URL}{OLLAMA_GENERATE_ENDPOINT_SUFFIX}", json=payload, timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        response_data = response.json()
        duration = time.perf_counter() - start_time
        return response_data.get("response", "Error: No 'response' key in Ollama's output.").strip(), duration
    except requests.exceptions.RequestException as e:
        duration = time.perf_counter() - start_time
        return f"Error: Request to Ollama failed: {e}", duration
    except Exception as e:
        duration = time.perf_counter() - start_time
        return f"Error: An unexpected error occurred: {e}", duration

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
    def log_test_case(self, model_name: str, test_case: Dict[str, Any], system_prompt: str, llm_response: str, duration: float):
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
            f"\nLLM RESPONSE:\n{llm_response}",
            f"\nEXPECTED SHORT ANSWER:\n{test_case['expected_short_answer']}",
            f"\n--- End of Test Case ---\n" + "="*50 + "\n\n"
        ]
        try:
            with open(self.log_filepath, 'a', encoding='utf-8') as f: f.write("\n".join(log_entry))
        except IOError as e: print(f"[ERROR] Could not write to log file: {e}")
    def log_summary(self, models_tested: List[str], num_tests: int):
        if not self.log_filepath: return
        summary = ["--- Run Summary ---"]
        for model_name in models_tested:
            timings = self.model_timings.get(model_name, [])
            if timings:
                avg_time = sum(timings) / len(timings)
                total_time = sum(timings)
                summary.append(f"\nModel: {model_name}\n  - Total Tests: {len(timings)}\n  - Total Time Spent in LLM Calls: {total_time:.2f} seconds\n  - Average Response Time: {avg_time:.2f} seconds")
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


# --- FUNÇÃO PRINCIPAL DO TESTADOR ---

def main():
    print("--- Cybersecurity Knowledge Sanity Tester ---")
    
    available_models = list_ollama_models()
    if not available_models: return

    run_all = beaupy.confirm("Do you want to test ALL available models?", default_is_yes=False)
    
    models_to_test: List[str] = []
    if run_all:
        models_to_test = available_models
        print(f"[INFO] Selected all {len(models_to_test)} models for testing.")
    else:
        selected_model = beaupy.select(available_models, cursor="> ", cursor_style="cyan")
        if selected_model: models_to_test.append(selected_model)
        else:
            print("No model selected. Exiting.")
            return

    run_mode_key = "all_models" if run_all else re.sub(r'[^a-zA-Z0-9]', '_', models_to_test[0])
    logger = TestLogger()
    logger.initialize(run_mode_key)

    system_prompt_for_tests = "You are a helpful assistant specialized in cybersecurity topics. Answer the user's question directly and concisely."

    all_results_for_json = {}

    for model_name in models_to_test:
        print(f"\n" + "#"*20 + f" TESTING MODEL: {model_name} " + "#"*20)
        all_results_for_json[model_name] = {}
        
        for i, test_case in enumerate(TEST_CASES):
            print(f"\n--- Running Test {i+1}/{len(TEST_CASES)}: [{test_case['category']}] ---")
            print(f"  Prompt > {test_case['prompt']}")

            llm_response, duration = call_ollama(model_name, test_case['prompt'], system_prompt_for_tests)
            
            # Apresentar resultados no ecrã para avaliação humana
            print("\n" + "-"*15 + "  LLM RESPONSE  " + "-"*15)
            print(llm_response)
            print(f"(Response time: {duration:.2f} seconds)")
            print("-" * (32 + len("LLM RESPONSE")))

            print("\n" + "-"*15 + "  EXPECTED INFO  " + "-"*15)
            print(f"Expected Answer (Short): {test_case['expected_short_answer']}")
            print(f"Expected Keywords: {', '.join(test_case['expected_keywords'])}")
            print(f"Source/More Info: {test_case['source_url']}")
            print("-" * (32 + len("EXPECTED INFO")))
            
            logger.log_test_case(model_name, test_case, system_prompt_for_tests, llm_response, duration)
            
            # <<< ALTERAÇÃO: Adicionar mais campos ao JSON para o script de análise
            all_results_for_json[model_name][test_case['category']] = {
                "prompt": test_case['prompt'],
                "expected_short_answer": test_case['expected_short_answer'],
                "llm_response": llm_response,
                "evaluation": "Correct",  # Valor por defeito
                "analysis": ""
            }
            
            print("\n" + "*"*60)

    logger.log_summary(models_to_test, len(TEST_CASES))
    save_results_to_json(all_results_for_json, RESULTS_JSON_FILENAME)
    print("\n--- Testing complete. Check log file for a full record. ---")
    print(f"--- A 'Results.json' file has been created. You can now run the analysis script. ---")


if __name__ == "__main__":
    main()