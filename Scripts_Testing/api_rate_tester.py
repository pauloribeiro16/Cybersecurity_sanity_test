import os
import json
import re
import time
import requests
from typing import Tuple, Optional

# --- CONFIGURAÇÕES E SEGREDOS ---
# Carregar segredos a partir de variáveis de ambiente para segurança
API_ENDPOINT = os.getenv("EVAL_API_ENDPOINT")
API_KEY = os.getenv("EVAL_API_KEY")
CHANNEL_ID = os.getenv("EVAL_CHANNEL_ID")
THREAD_ID = os.getenv("EVAL_THREAD_ID")

# --- CONFIGURAÇÕES DO TESTE DE FREQUÊNCIA ---

# Um prompt de teste simples para enviar à API
TEST_PROMPT = "This is a simple test prompt to check API responsiveness. Please respond with 'OK'."

# Número de pedidos a fazer em cada teste de intervalo
REQUESTS_PER_INTERVAL_TEST = 10

# Intervalos (em segundos) para testar. Começa com um intervalo maior e vai diminuindo.
INTERVALS_TO_TEST =[60]

# --- FUNÇÕES CORE ---

def check_secrets() -> bool:
    """Verifica se todas as variáveis de ambiente necessárias estão definidas."""
    if not all([API_ENDPOINT, API_KEY, CHANNEL_ID, THREAD_ID]):
        print("\n[ERROR] Uma ou mais variáveis de ambiente da API de avaliação não estão definidas.")
        print("Por favor, defina EVAL_API_ENDPOINT, EVAL_API_KEY, EVAL_CHANNEL_ID, e EVAL_THREAD_ID.")
        return False
    return True

def call_api_once(prompt: str) -> Tuple[bool, str]:
    """
    Faz uma única chamada à API e verifica se foi bem-sucedida.
    Retorna (True, "Success") ou (False, "Error Message").
    """
    form_data = {
        "channel_id": CHANNEL_ID, "thread_id": THREAD_ID,
        "user_info": "{}", "message": prompt,
    }
    headers = {'x-api-key': API_KEY}

    try:
        # Usamos um timeout mais curto aqui, pois só queremos saber se o pedido foi aceite
        response = requests.post(API_ENDPOINT, headers=headers, data=form_data, timeout=60)
        response.raise_for_status()
        response_text = response.text.strip()

        # Verifica a presença da mensagem de erro específica da API
        if '"Error invoking model, please try again later..."' in response_text:
            return False, "API Error: Error invoking model"

        # Verifica se a resposta contém algum conteúdo útil (não apenas eventos de 'start'/'done')
        if '"type": "message"' in response_text or '"type": "token"' in response_text:
            return True, "Success"
        else:
            return False, "API Error: No content in response"

    except requests.exceptions.Timeout:
        return False, "Network Error: Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Network Error: {e}"

def main():
    """Função principal para executar o teste de frequência da API."""
    if not check_secrets():
        return

    print("--- API Rate Limit Tester ---")
    print(f"Cada teste fará {REQUESTS_PER_INTERVAL_TEST} pedidos para um determinado intervalo.")
    print("O objetivo é encontrar o menor intervalo que não resulta em erros da API.\n")

    successful_intervals = []

    for interval in INTERVALS_TO_TEST:
        print(f"\n--- A testar intervalo: {interval:.2f} segundos ---")
        
        error_count = 0
        success_count = 0

        for i in range(REQUESTS_PER_INTERVAL_TEST):
            print(f"  Enviando pedido {i + 1}/{REQUESTS_PER_INTERVAL_TEST}...", end="", flush=True)
            
            is_success, status_message = call_api_once(TEST_PROMPT)

            if is_success:
                success_count += 1
                print(f" Sucesso!")
            else:
                error_count += 1
                print(f" FALHA! ({status_message})")

            # Espera o intervalo definido antes do próximo pedido
            if i < REQUESTS_PER_INTERVAL_TEST - 1:
                time.sleep(interval)

        # Avalia o resultado do teste para este intervalo
        print(f"\n  Resultado para o intervalo de {interval:.2f}s: {success_count} sucessos, {error_count} falhas.")
        
        if error_count == 0:
            print("  [STATUS] Este intervalo parece ser seguro.")
            successful_intervals.append(interval)
        else:
            failure_rate = (error_count / REQUESTS_PER_INTERVAL_TEST) * 100
            print(f"  [STATUS] Este intervalo é instável ({failure_rate:.0f}% de falha). A parar os testes.")
            break # Para o teste assim que encontrar um intervalo com falhas

    print("\n--- Resultados Finais ---")
    if not successful_intervals:
        print("Nenhum intervalo foi consistentemente bem-sucedido.")
        print("A API pode estar offline ou com limites de frequência muito restritos.")
        print("Tente aumentar os intervalos no array 'INTERVALS_TO_TEST' no script.")
    else:
        # O melhor intervalo é o mais pequeno que foi bem-sucedido
        best_interval = min(successful_intervals)
        print(f"Intervalos bem-sucedidos testados: {successful_intervals}")
        print(f"\n[RECOMENDAÇÃO]")
        print(f"O intervalo mais rápido e seguro encontrado foi de {best_interval:.2f} segundos entre os pedidos.")
        print(f"Considere usar um valor ligeiramente superior (ex: {best_interval + 0.2:.2f}s) no seu script principal para uma margem de segurança.")

if __name__ == "__main__":
    main()