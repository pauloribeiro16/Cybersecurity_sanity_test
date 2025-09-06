# cybersecurity_inference_tester.py

import os
import datetime
import re
import time
from typing import List, Dict, Optional, Any, Tuple

# --- DEPENDÊNCIAS ---
# pip install requests
import requests

# --- CONFIGURAÇÕES ---

OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_TAGS_ENDPOINT_SUFFIX = "/tags"
OLLAMA_GENERATE_ENDPOINT_SUFFIX = "/generate"
OLLAMA_REQUEST_TIMEOUT_SECONDS = 3000
OLLAMA_KEEP_ALIVE_DURATION = "5m"

LOG_DIR_NAME = "cybersecurity_inference_logs" # Pasta de logs separada
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Modelos e Prompt para o Teste de Inferência ---

# Modelos de topo selecionados para o teste aprofundado
MODELS_TO_TEST = [
    "gpt-oss:20b"
]

# Prompt "Chain-of-Thought" para forçar o raciocínio explícito
SYSTEM_PROMPT = "You are an expert cybersecurity analyst. First, think step-by-step to break down the user's question. Explain your reasoning process. Finally, provide a clear and direct answer."


# --- CASOS DE TESTE DE INFERÊNCIA ---
TEST_CASES = [
    # --- Categoria: Raciocínio Dedutivo (Causa-Efeito) ---
    {
        "category": "Inference - Deductive Reasoning",
        "prompt": "An analyst observes: 1) A key web server's CPU is at 100%. 2) Logs show massive login requests from thousands of IPs to the admin page. 3) No logins succeed. What is the most likely cyberattack type, and which two elements of the CIA triad are primarily targeted?",
        "evaluation_guidelines": "A resposta deve identificar o ataque como Denial of Service (DoS) ou Brute-Force/Credential Stuffing. Deve ligar o esgotamento de recursos à 'Availability' e a tentativa de acesso a contas à 'Confidentiality'."
    },
    {
        "category": "Inference - Deductive Reasoning",
        "prompt": "The CFO receives a convincing email from the 'CEO' asking for an urgent wire transfer. The CFO complies. Later, it's discovered the CEO never sent it. In the STRIDE model, what is the primary threat category demonstrated? Which NIST CSF function covers the actions needed *after* the money is sent?",
        "evaluation_guidelines": "A resposta deve identificar a ameaça STRIDE como 'Spoofing' (personificação). Deve identificar a função NIST CSF correta para as ações pós-incidente como 'Respond' (para contenção e investigação) e 'Recover' (para tentar reaver os fundos)."
    },
    {
        "category": "Inference - Deductive Reasoning",
        "prompt": "One week after a developer leaves the company, their account is used to access and exfiltrate a sensitive code repository. Which two security control domains most likely failed? What fundamental security principle was violated regarding user account management?",
        "evaluation_guidelines": "A resposta deve identificar as falhas nos controlos de 'Identity and Access Management (IAM)' e 'Offboarding Procedures'. Deve referir a violação do princípio de 'Least Privilege' ou a falha na 'revogação de acesso atempada'."
    },
    # --- Categoria: Análise Comparativa (Trade-offs) ---
    {
        "category": "Inference - Comparative Analysis",
        "prompt": "A team is deciding between a Web Application Firewall (WAF) and Runtime Application Self-Protection (RASP) to protect a custom application. Compare the two based on their deployment location and detection method. Which is better at stopping zero-day attacks and why?",
        "evaluation_guidelines": "Deve explicar que o WAF é um controlo de rede (externo) que inspeciona o tráfego HTTP, enquanto o RASP é instrumentado dentro da aplicação (interno). Deve concluir que o RASP é teoricamente melhor para zero-days porque tem contexto da execução da aplicação, ao contrário do WAF que depende de assinaturas/padrões."
    },
    {
        "category": "Inference - Comparative Analysis",
        "prompt": "A critical vulnerability is found in a production system. The team can either take the system offline for an emergency patch, risking business downtime, or apply a virtual patch via their IPS. Explain the trade-off between these two actions in terms of risk reduction and operational impact.",
        "evaluation_guidelines": "Deve explicar que o 'emergency patch' é uma solução completa mas com alto impacto operacional (downtime). O 'virtual patch' é uma mitigação rápida com baixo impacto operacional, mas que não corrige a vulnerabilidade subjacente, sendo uma solução temporária. A resposta deve focar no balanço entre segurança e continuidade do negócio."
    },
    {
        "category": "Inference - Comparative Analysis",
        "prompt": "A FinTech startup processes credit card data and also wants to demonstrate strong overall security practices to investors. Should they prioritize achieving PCI DSS compliance or ISO 27001 certification first? Justify your choice.",
        "evaluation_guidelines": "A resposta deve argumentar que a PCI DSS deve ser a prioridade, pois é um requisito *obrigatório* para processar cartões de crédito. A ISO 27001 é um framework de gestão de segurança mais vasto e voluntário, sendo um excelente segundo passo para demonstrar maturidade, mas a PCI DSS é uma necessidade legal/contratual imediata."
    },
    # --- Categoria: Planeamento e Sequenciamento ---
    {
        "category": "Inference - Planning & Sequencing",
        "prompt": "Your company discovers it's vulnerable to Log4Shell (CVE-2021-44228) on internet-facing servers. Using the NIST CSF: 1) What is one immediate 'Respond' action? 2) What is one immediate 'Protect' action? 3) What fundamental principle of the CIA triad is most at risk?",
        "evaluation_guidelines": "1) Respond: Isolar os sistemas afetados da rede. 2) Protect: Aplicar uma regra de bloqueio na WAF/IPS para assinaturas conhecidas do Log4Shell. 3) CIA Triad: 'Confidentiality' e 'Integrity' estão em risco devido à possibilidade de RCE (Remote Code Execution)."
    },
    {
        "category": "Inference - Planning & Sequencing",
        "prompt": "A startup is building its first cloud-native mobile application. Outline the first THREE security activities they should integrate into their software development lifecycle (SDLC) from day one.",
        "evaluation_guidelines": "Uma boa resposta deve priorizar atividades proativas e de base. Exemplos excelentes incluem: 1) Threat Modeling (para pensar em ameaças antes de codificar), 2) Dependency Scanning / SCA (para evitar vulnerabilidades em bibliotecas de terceiros), 3) Secure Coding Training/Guidelines para os developers."
    },
    {
        "category": "Inference - Planning & Sequencing",
        "prompt": "A company just recovered from a major data breach. The systems are back online. What are the two most critical activities within the 'Recover' function of the NIST CSF that they must now perform, beyond just restoring data?",
        "evaluation_guidelines": "A resposta deve focar nas atividades pós-restauração. Deve mencionar: 1) Conduzir uma investigação 'root cause analysis' / 'lessons learned' para entender como a falha aconteceu e evitar que se repita. 2) Melhorar os processos e controlos de segurança com base nas descobertas (ex: novas políticas, treinos, ferramentas)."
    }
]


# --- MÓDULO DE INTERAÇÃO COM OLLAMA (Sem alterações) ---

def call_ollama(model_name: str, user_prompt: str, system_prompt: str) -> Tuple[str, float]:
    """Chama a API do Ollama e retorna a resposta e o tempo de duração da chamada."""
    payload = {
        "model": model_name,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "keep_alive": OLLAMA_KEEP_ALIVE_DURATION,
        "options": {
             "enable_thinking": False
        }
    }

    
    start_time = time.perf_counter()
    try:
        response = requests.post(
            f"{OLLAMA_API_BASE_URL}{OLLAMA_GENERATE_ENDPOINT_SUFFIX}",
            json=payload,
            timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS
        )
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

# --- MÓDULO DE LOGGING SIMPLIFICADO (Sem alterações) ---

class TestLogger:
    def __init__(self):
        self.log_filepath: Optional[str] = None
        self.model_timings: Dict[str, List[float]] = {}

    def initialize(self, run_mode_key: str):
        log_dir = os.path.join(SCRIPT_DIR, LOG_DIR_NAME)
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filepath = os.path.join(log_dir, f"test_run_{run_mode_key}_{timestamp}.txt")
        header = f"Cybersecurity Inference Test Log\nRun Mode: {run_mode_key}\nInitialized: {datetime.datetime.now().isoformat()}\n" + "="*50 + "\n\n"
        try:
            with open(self.log_filepath, 'w', encoding='utf-8') as f:
                f.write(header)
            print(f"[INFO] Log file initialized at: {self.log_filepath}")
        except IOError as e:
            print(f"[ERROR] Could not create log file: {e}")
            self.log_filepath = None
    
    def log_test_case(self, model_name: str, test_case: Dict[str, Any], system_prompt: str, llm_response: str, duration: float):
        if not self.log_filepath:
            return
        
        if model_name not in self.model_timings:
            self.model_timings[model_name] = []
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
            f"\n--- End of Test Case ---\n" + "="*50 + "\n\n"
        ]
        try:
            with open(self.log_filepath, 'a', encoding='utf-8') as f:
                f.write("\n".join(log_entry))
        except IOError as e:
            print(f"[ERROR] Could not write to log file: {e}")

    def log_summary(self, models_tested: List[str], num_tests: int):
        if not self.log_filepath:
            return
        
        summary = ["--- Run Summary ---"]
        for model_name in models_tested:
            timings = self.model_timings.get(model_name, [])
            if timings:
                avg_time = sum(timings) / len(timings)
                total_time = sum(timings)
                summary.append(
                    f"\nModel: {model_name}\n"
                    f"  - Total Tests: {len(timings)}\n"
                    f"  - Total Time Spent in LLM Calls: {total_time:.2f} seconds\n"
                    f"  - Average Response Time: {avg_time:.2f} seconds"
                )
        summary.append(f"\nTotal Number of Test Cases Configured: {num_tests}")
        summary.append(f"\nEnd of Log.")
        
        try:
            with open(self.log_filepath, 'a', encoding='utf-8') as f:
                f.write("\n".join(summary))
        except IOError as e:
            print(f"[ERROR] Could not write summary to log file: {e}")

# --- FUNÇÃO PRINCIPAL DO TESTADOR ---

def main():
    print("--- Cybersecurity Inference Tester ---")
    print(f"Models to be tested: {', '.join(MODELS_TO_TEST)}")
    
    run_mode_key = "inference_run"
    logger = TestLogger()
    logger.initialize(run_mode_key)

    for model_name in MODELS_TO_TEST:
        print(f"\n" + "#"*20 + f" TESTING MODEL: {model_name} " + "#"*20)
        
        for i, test_case in enumerate(TEST_CASES):
            print(f"\n--- Running Test {i+1}/{len(TEST_CASES)}: [{test_case['category']}] ---")
            print(f"  Prompt > {test_case['prompt']}")

            llm_response, duration = call_ollama(model_name, test_case['prompt'], SYSTEM_PROMPT)
            
            print("\n" + "-"*15 + "  LLM RESPONSE  " + "-"*15)
            print(llm_response)
            print(f"(Response time: {duration:.2f} seconds)")
            print("-" * (32 + len("LLM RESPONSE")))

            print("\n" + "-"*15 + "  EVALUATION GUIDELINES  " + "-"*15)
            print(test_case['evaluation_guidelines'])
            print("-" * (32 + len("EVALUATION GUIDELINES")))
            
            logger.log_test_case(model_name, test_case, SYSTEM_PROMPT, llm_response, duration)
            
            print("\n" + "*"*60)

    logger.log_summary(MODELS_TO_TEST, len(TEST_CASES))
    print(f"\n--- Testing complete. Check the '{LOG_DIR_NAME}' directory for the full log file. ---")


if __name__ == "__main__":
    main()