import os
import time
import requests
from typing import Tuple, Optional

# --- CONFIGURAÇÕES E SEGREDOS ---
# Carregar segredos a partir de variáveis de ambiente para segurança
API_ENDPOINT = os.getenv("EVAL_API_ENDPOINT")
API_KEY = os.getenv("EVAL_API_KEY")

# --- FUNÇÕES CORE ---

def check_secrets() -> bool:
    """Verifica se todas as variáveis de ambiente necessárias estão definidas."""
    if not all([API_ENDPOINT, API_KEY]):
        print("\n[ERRO] Uma ou mais variáveis de ambiente da API não estão definidas.")
        print("Por favor, defina EVAL_API_ENDPOINT e EVAL_API_KEY.")
        return False
    return True

def run_sanity_check() -> Tuple[bool, str]:
    """
    Faz uma única chamada GET simples à API para verificar a conectividade e autenticação.
    Retorna (True, "Mensagem de Sucesso") ou (False, "Mensagem de Erro").
    """
    headers = {'x-api-key': API_KEY}

    try:
        print(f"A enviar um pedido GET para: {API_ENDPOINT}")
        # Usamos um timeout de 15 segundos para a verificação de sanidade.
        response = requests.get(API_ENDPOINT, headers=headers, timeout=15)
        
        # A API pode retornar 403 (Forbidden) se um GET não for permitido, mas a chave for válida.
        # Consideramos sucesso se não for um erro de cliente (401 Unauthorized) ou de servidor.
        if response.status_code == 401:
            return False, f"Falha de Autenticação (Código {response.status_code}). Verifique a sua API Key."
        
        response.raise_for_status()
        
        return True, f"Sucesso! A API respondeu com o código de status: {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Erro de Rede: O pedido excedeu o tempo limite (Timeout)."
    except requests.exceptions.HTTPError as e:
        return False, f"Erro HTTP: A API retornou um código de erro {e.response.status_code}. Resposta: {e.response.text[:100]}"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de Rede: Não foi possível conectar à API. Detalhes: {e}"

def main():
    """Função principal para executar o teste de sanidade da API."""
    if not check_secrets():
        return

    print("\n--- Verificação de Sanidade da API ---")
    
    is_success, status_message = run_sanity_check()

    if is_success:
        print(f"\n[OK] {status_message}")
        print("A conectividade com a API e a chave parecem estar a funcionar corretamente.")
    else:
        print(f"\n[FALHA] {status_message}")
        print("Verifique o endpoint da API, a sua chave e a sua conexão de rede.")

if __name__ == "__main__":
    main()