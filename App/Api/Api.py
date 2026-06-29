import os
import requests
from dotenv import load_dotenv

caminho_env = os.path.join("App", ".env")
load_dotenv(dotenv_path=caminho_env)

# Carrega o token uma única vez
MEU_TOKEN = os.getenv("COSMOS_API_TOKEN")

def obter_nome_produto(gtin):
    if not MEU_TOKEN:
        return "Erro: A chave da API não foi encontrada no .env."

    url = f"https://api.cosmos.bluesoft.com.br/gtins/{gtin}.json"
    
    headers = {
        "X-Cosmos-Token": MEU_TOKEN,
        "User-Agent": "MeuAppConsulta/1.0", 
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            dados_json = response.json()
            return dados_json.get("description")
            
        elif response.status_code == 404:
            return "Produto não encontrado."
            
        else:
            return f"Erro na requisição. Código HTTP: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro de conexão: {e}"