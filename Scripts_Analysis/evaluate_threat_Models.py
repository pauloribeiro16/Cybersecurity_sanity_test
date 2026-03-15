import os
import json
import re
import time
import beaupy
import datetime
from typing import List, Dict, Optional, Tuple

# --- DEPENDÊNCIAS ---
# pip install requests beaupy
import requests

# --- CONFIGURAÇÕES E SEGREDOS ---
RESULTS_ROOT_DIR = "ResultsThreatModeling"

# Carregar segredos a partir de variáveis de ambiente para segurança
API_ENDPOINT = os.getenv("EVAL_API_ENDPOINT")
API_KEY = os.getenv("EVAL_API_KEY")
CHANNEL_ID = os.getenv("EVAL_CHANNEL_ID")
THREAD_ID = os.getenv("EVAL_THREAD_ID")

# --- PROMPTS DE AVALIAÇÃO COM RUBRICAS E FORMATO ESTRUTURADO ---

PROMPT_THREAT_IDENTIFICATION = """
**EVALUATION TASK**
You are an expert cybersecurity evaluator. Your task is to score a language model's response based on the provided rubric. Score from 1 (Poor) to 5 (Excellent).

**RESPONSE FORMAT:**
You MUST respond ONLY in the following two-line format. Do not add any other text before or after the response.
Score: [Your integer score from 1 to 5]
Justification: [Your brief, one or two sentence justification for the score.]

**SCORING RUBRIC (Threat Identification):**
- **Score 1 (Poor):** The response identifies irrelevant, generic, or incorrect threats.
- **Score 2 (Weak):** The response identifies a plausible but low-priority threat, or describes a primary threat superficially.
- **Score 3 (Acceptable):** The response correctly identifies at least one of the most obvious, primary threats.
- **Score 4 (Good):** The response identifies multiple primary threats and explains why they are relevant to the specific architecture.
- **Score 5 (Excellent):** The response identifies primary threats and also includes a more subtle or second-order threat.

**SCENARIO CONTEXT:**
{architecture_description}

**MODEL'S RESPONSE TO EVALUATE:**
{model_response}

**YOUR EVALUATION:**
"""

PROMPT_MITIGATION_QUALITY = """
**EVALUATION TASK**
You are an expert cybersecurity evaluator. Your task is to score a language model's proposed mitigations based on the provided rubric. Score from 1 (Poor) to 5 (Excellent).

**RESPONSE FORMAT:**
You MUST respond ONLY in the following two-line format. Do not add any other text before or after the response.
Score: [Your integer score from 1 to 5]
Justification: [Your brief, one or two sentence justification for the score.]

**SCORING RUBRIC (Mitigation Quality):**
- **Score 1 (Poor):** The proposal is a vague, non-actionable statement.
- **Score 2 (Weak):** The proposal suggests a type of control but is not specific or is suboptimal.
- **Score 3 (Acceptable):** The proposal correctly names the appropriate security control but lacks implementation details.
- **Score 4 (Good):** The proposal is specific, actionable, and follows industry best practices.
- **Score 5 (Excellent):** The proposal describes a multi-layered (defense-in-depth) solution.

**SCENARIO CONTEXT:**
{architecture_description}

**MODEL'S RESPONSE TO EVALUATE:**
{model_response}

**YOUR EVALUATION:**
"""

# --- FUNÇÕES CORE ---

def check_secrets():
    """Verifica se todas as variáveis de ambiente necessárias estão definidas."""
    if not all([API_ENDPOINT, API_KEY, CHANNEL_ID, THREAD_ID]):
        print("\n[ERROR] Uma ou mais variáveis de ambiente da API de avaliação não estão definidas.")
        print("Por favor, defina EVAL_API_ENDPOINT, EVAL_API_KEY, EVAL_CHANNEL_ID, e EVAL_THREAD_ID.")
        return False
    return True

def find_unevaluated_files(root_dir: str) -> List[str]:
    """Encontra todos os ficheiros ThreatModel_Results.json que ainda não foram totalmente avaliados."""
    unevaluated_files = []
    if not os.path.isdir(root_dir):
        print(f"[ERROR] O diretório de resultados '{root_dir}' não foi encontrado.")
        return [] # Retorna lista vazia se o diretório não existir
        
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "ThreatModel_Results.json":
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    for result in data.get("results", {}).values():
                        if result.get("manual_evaluation", {}).get("threat_identification_score") is None:
                            unevaluated_files.append(filepath)
                            break
                except (json.JSONDecodeError, KeyError):
                    print(f"[WARNING] A ignorar o ficheiro corrompido ou malformado: {filepath}")
                    continue
    return unevaluated_files

def call_evaluation_api(prompt: str) -> Tuple[Optional[int], Optional[str], str]:
    """Chama a API de avaliação, espera pelo resultado e extrai a pontuação e justificação."""
    form_data = {
        "channel_id": CHANNEL_ID, "thread_id": THREAD_ID,
        "user_info": "{}", "message": prompt,
    }
    headers = {'x-api-key': API_KEY}
    
    max_retries = 3
    for attempt in range(max_retries):
        print(f"    [LOG] A iniciar chamada POST para a API (Tentativa {attempt + 1}/{max_retries}, Timeout: 180s)...")
        try:
            # Faz uma única chamada POST com um timeout longo para esperar pela resposta completa
            response = requests.post(API_ENDPOINT, headers=headers, data=form_data, timeout=180)
            print(f"    [LOG] Resposta recebida com código de status: {response.status_code}")
            response.raise_for_status()
            
            response_text = response.text.strip()
            print(f"    [LOG] Resposta completa da API (texto bruto):\n---\n{response_text}\n---")

            # Verifica se há um erro explícito da API
            if '"Error invoking model, please try again later..."' in response_text:
                print("    [WARNING] A API retornou um erro explícito: 'Error invoking model'.")
                raise requests.exceptions.RequestException("API returned a model invocation error.")

            # Tenta encontrar a mensagem final completa no evento 'message'
            message_match = re.search(r'{"type": "ai", "content": "(.+?)"', response_text)
            if message_match:
                # Descodifica a string JSON interna
                final_message = json.loads(f'"{message_match.group(1)}"')
                print(f"    [LOG] Mensagem final reconstruída a partir do evento 'message': {final_message}")
            else:
                print("    [LOG] Evento 'message' não encontrado, a tentar reconstruir a partir de 'token's.")
                tokens = re.findall(r'{"run_id": "[^"]+", "type": "token", "content": "([^"]*)"}', response_text)
                final_message = "".join(tokens)
                final_message = final_message.encode().decode('unicode_escape')
                print(f"    [LOG] Mensagem final reconstruída a partir de 'token's: {final_message}")

            # Extrair a pontuação e a justificação da mensagem reconstruída
            score_match = re.search(r"Score:\s*([1-5])", final_message, re.IGNORECASE)
            score = int(score_match.group(1)) if score_match else None
            
            just_match = re.search(r"Justification:\s*(.+)", final_message, re.IGNORECASE | re.DOTALL)
            justification = just_match.group(1).strip() if just_match else None

            if score is not None:
                print("    [LOG] Pontuação extraída com sucesso.")
                return score, justification, response_text
            else:
                print("    [WARNING] Não foi possível extrair a PONTUAÇÃO da resposta. A tentar novamente...")
                # Força uma nova tentativa se a pontuação não for encontrada
                raise requests.exceptions.RequestException("Score not found in response.")

        except requests.exceptions.RequestException as e:
            print(f"    [ERROR] Falha na tentativa {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                sleep_time = 25  # Espera 5s, 10s, 20s... (Exponential Backoff)
                sleep_time = 5 * (2 ** attempt)  # Espera 5s, 10s, 20s... (Exponential Backoff)
                print(f"    A aguardar {sleep_time} segundos antes de tentar novamente...")
                time.sleep(sleep_time)
            else:
                print("    [ERROR] Número máximo de tentativas atingido. A desistir desta avaliação.")
                return None, None, f"API call failed after {max_retries} retries."
    
    return None, None, "Failed after all retries."

def main():
    """Função principal para executar o processo de avaliação."""
    if not check_secrets():
        return

    print("--- Automatic Threat Model Evaluator ---")
    
    unevaluated_files = find_unevaluated_files(RESULTS_ROOT_DIR)
    if not unevaluated_files:
        print("\nNenhum ficheiro de resultados por avaliar foi encontrado. Bom trabalho!")
        return

    print(f"\nForam encontrados {len(unevaluated_files)} ficheiros com cenários por avaliar.")
    if not beaupy.confirm("Deseja iniciar a avaliação automática agora?", default_is_yes=True):
        print("Avaliação cancelada.")
        return

    for filepath in unevaluated_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"\n[ERROR] Não foi possível ler ou processar o ficheiro {filepath}: {e}"); continue

        model_name = data.get("model_name", "Unknown Model")
        print("\n" + "="*20 + f" A AVALIAR: {model_name} " + "="*20)
        print(f"Ficheiro: {filepath}")

        has_changes = False
        results = data.get("results", {})
        
        for test_id, result in results.items():
            evaluation = result.get("manual_evaluation", {})
            
            if evaluation.get("threat_identification_score") is None:
                has_changes = True
                print(f"\n--- Cenário: {test_id} ({result.get('title')}) ---")

                # --- 1. Avaliar Identificação de Ameaças ---
                print("  -> A avaliar a identificação de ameaças...")
                model_response_q1 = result["model_responses"]["Q1_Identify"]
                eval_prompt_q1 = PROMPT_THREAT_IDENTIFICATION.format(
                    architecture_description=result["architecture_description"],
                    model_response=model_response_q1
                )
                
                score_q1, just_q1, raw_resp_q1 = call_evaluation_api(eval_prompt_q1)
                evaluation["evaluator_raw_response_q1"] = raw_resp_q1 # Guardar resposta bruta
                if score_q1 is not None:
                    evaluation["threat_identification_score"] = score_q1
                    evaluation["threat_identification_justification"] = just_q1
                    print(f"  -> Pontuação de Identificação de Ameaças: {score_q1}/5")
                time.sleep(2)

                # --- 2. Avaliar Qualidade das Mitigações ---
                print("  -> A avaliar a qualidade das mitigações...")
                model_response_q2 = result["model_responses"]["Q2_Mitigate"]
                eval_prompt_q2 = PROMPT_MITIGATION_QUALITY.format(
                    architecture_description=result["architecture_description"],
                    model_response=model_response_q2
                )

                score_q2, just_q2, raw_resp_q2 = call_evaluation_api(eval_prompt_q2)
                evaluation["evaluator_raw_response_q2"] = raw_resp_q2 # Guardar resposta bruta
                if score_q2 is not None:
                    evaluation["mitigation_quality_score"] = score_q2
                    evaluation["mitigation_quality_justification"] = just_q2
                    print(f"  -> Pontuação de Qualidade das Mitigações: {score_q2}/5")
                time.sleep(2)

                evaluation["notes"] = f"Automatically evaluated on {datetime.datetime.now().isoformat()}"
                data["results"][test_id]["manual_evaluation"] = evaluation
            
        if has_changes:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"\n[SUCCESS] O ficheiro de resultados para {model_name} foi atualizado com as novas avaliações.")
            except IOError as e:
                print(f"\n[ERROR] Não foi possível guardar o ficheiro atualizado {filepath}: {e}")

    print("\n--- Processo de avaliação automática concluído. ---")

if __name__ == "__main__":
    main()