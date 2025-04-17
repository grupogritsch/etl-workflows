import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

TOKEN = 'nCFA1rinSPamjFg6mHsstLy88VSswJoKRJ1mjiBsryuAD8RMuLKKxQ'
DOMAIN = 'https://gritsch.eslcloud.com.br/api'
PATH_DATASETS = Variable.get("PATH_DATASETS")

def retornar_datas():
    """Retorna as datas no formato esperado."""
    ontem = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')
    ano = (datetime.now() - timedelta(days=365)).strftime('%d/%m/%Y')
    return {
        "PERIODO": f'{ontem} - {ontem}',
        "ATUALIZACAO": f'{ano} - {ontem}'
    }

DATAS = retornar_datas()

def criar_payload(tipo, **kwargs):
    """Cria a estrutura de payload com parâmetros dinâmicos."""
    return {
        "export_to_ftp": False,
        "search": {tipo: {key: value for key, value in kwargs.items() if value}}
    }

FRETES = {
    "Fretes": criar_payload("freights", service_at=DATAS["PERIODO"]),
    "FretesAtores": criar_payload("freights", service_at=DATAS["PERIODO"]),
    "FretesConferencias": criar_payload("check_in_orders", started_at=DATAS["ATUALIZACAO"], updated_at=DATAS["PERIODO"]),
    "FretesDinamico": criar_payload("freights", service_at=DATAS["ATUALIZACAO"], updated_at=DATAS["PERIODO"]),
    "FretesFaturas": criar_payload("accounting_credits", issue_date=DATAS["ATUALIZACAO"], updated_at=DATAS["PERIODO"]),
    "FretesManifestos": criar_payload("manifests", service_at=DATAS["ATUALIZACAO"], updated_at=DATAS["PERIODO"]),
    "FretesOcorrencias": criar_payload("invoice_occurrences", occurrence_at=DATAS["PERIODO"]),       
    #"FretesExcluidos": criar_payload("freights", deleted_at=DATAS["PERIODO"])
}

def obter_payload(nome):
    """Retorna o payload solicitado ou uma mensagem de erro se não existir."""
    return FRETES.get(nome, f"Frete '{nome}' não encontrado.")

def solicitar_relatorio(filename, id_relatorio):
    """Solicita a geração de um relatório via API."""
    endpoint = f'{DOMAIN}/analytics/reports/{id_relatorio}/export'
    payload = obter_payload(filename)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code != 200:
            return {'error': f'Falha na requisição. Código: {response.status_code}, Resposta: {response.text}'}
        return response.json().get('id', {'error': 'ID ausente na resposta do servidor'})
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def buscar_url_arquivo(**kwargs):
    """Obtém a URL de download do relatório."""
    ti = kwargs["ti"]
    id_arquivo = ti.xcom_pull(task_ids='tsk_solicitar_relatorio')
    print(id_arquivo)
    endpoint = f'{DOMAIN}/analytics/report_files/{id_arquivo}'
    print(endpoint)
    headers = {'Authorization': f'Bearer {TOKEN}'}
    while True:
        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code != 200:
                return {'error': f'Falha na requisição. Código: {response.status_code}, Resposta: {response.text}'}
            data = response.json()
            if data.get('status') == 'error':
                return {'error': 'Erro no status do relatório', 'details': data}
            if not data.get('download_url'):
                time.sleep(120)
                continue
            return data.get('download_url')
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

def baixar_arquivo(filename, **kwargs):
    """Faz o download do arquivo gerado."""
    ti = kwargs["ti"]
    download_url = ti.xcom_pull(task_ids='tsk_buscar_url_arquivo')
    try:
        os.makedirs('/tmp', exist_ok=True)
        caminho_arquivo = os.path.join('/tmp', f"{filename}.xlsx")
        with requests.get(download_url, stream=True) as response:
            response.raise_for_status()
            with open(caminho_arquivo, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return caminho_arquivo
    except requests.exceptions.RequestException:
        return None

def xlsx_to_parquet(filename, **kwargs):
    """Converte um arquivo XLSX para parquet."""
    ti = kwargs["ti"]
    arquivo_xlsx = ti.xcom_pull(task_ids='tsk_baixar_arquivo')
    df = pd.read_excel(arquivo_xlsx, engine='openpyxl', dtype=str)
    df['Atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_parquet(f'{PATH_DATASETS}Raw_{filename}.parquet', engine='pyarrow', compression='snappy', index=False)
    return f'{PATH_DATASETS}Raw_{filename}.parquet'
