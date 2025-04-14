import requests
import hashlib
from requests.auth import HTTPBasicAuth
import pandas as pd
from airflow.models import Variable
from datetime import datetime

BASE_URL = "https://api.truckpag.com.br"
data_inicio = Variable.get("torre_transacoes_data_inicio")
data_fim = Variable.get("torre_transacoes_data_fim")
todas = Variable.get("torre_transacoes_todas")
PATH_DATASETS = Variable.get("PATH_DATASETS")


def gerar_token():
    login_endpoint = "/auth"
    usuario = "gritsch.bi"
    senha = "T$aNS/0RTE7GRI*&"

    # Gerar hash MD5 da senha
    senha_md5 = hashlib.md5(senha.encode()).hexdigest()

    # Fazer a requisição de autenticação
    url = f"{BASE_URL}{login_endpoint}"
    print(url)
    response = requests.post(url, auth=HTTPBasicAuth(usuario, senha_md5))

    # Verificar a resposta
    if response.status_code == 201:
        return response.json().get("token")
    else:
        print(f"Erro: {response.status_code} - {response.text}")

def consultar_api(tipo, **kwargs):
    ti = kwargs["ti"]
    token = ti.xcom_pull(task_ids='tsk_gerar_token')
    login_endpoint = "/Transacoes"
    if tipo == "diario":
        url = f"{BASE_URL}{login_endpoint}"
    elif tipo == "periodo":
        url = f"{BASE_URL}{login_endpoint}?dtini={data_inicio}&dtfim={data_fim}&todas={todas}"
    headers = {
        "Authorization": f"Bearer {token}", 
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": f"Erro {response.status_code}: {response.text}"}

def verificar_json_vazio(ti):
    json_dados = ti.xcom_pull(task_ids='tsk_consultar_api')

    if json_dados and json_dados.get("Transacoes"):
        return "tsk_json_to_parquet"
    else:
        return "tsk_notificar_json_vazio"

def notificar_json_vazio():
    print("JSON vazio")

def json_to_parquet(ti):
    json_dados = ti.xcom_pull(task_ids='tsk_consultar_api')
    if not json_dados or "Transacoes" not in json_dados:
        raise ValueError("Dados inválidos recebidos da API")
    transacoes = json_dados.get("Transacoes", [])
    df = pd.DataFrame(transacoes)
    df['Atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if df.empty:
        print("Nenhuma transação encontrada para inserir.")
        return
    df.to_parquet(f'{PATH_DATASETS}Raw_TorreTransacoes.parquet', engine='pyarrow', compression='snappy', index=False)

def parquet_to_raw():
    ...