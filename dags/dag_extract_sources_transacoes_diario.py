from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
import sys
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.append('/opt/airflow/')
from scripts.extract_sources_torre_transacoes import gerar_token, consultar_api, json_to_parquet, verificar_json_vazio, notificar_json_vazio

PATH_DATASETS = Variable.get("PATH_DATASETS")


default_args = {
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 15, 3, 0), 
    'email': ['fabio@gritsch.com.br'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    'ExtractSourcesTorreTransacoesDiario',
    tags=['TruckPag','API', 'Torre de Controle', 'Extracão', 'Diário', 'Sources'],
    default_args = default_args,
    schedule_interval='0 1 * * *',
    catchup = False,
) as dag:
    
    tsk_gerar_token = PythonOperator(
        task_id='tsk_gerar_token',
        python_callable=gerar_token,
        owner='César',
    )
    
    tsk_consultar_api = PythonOperator(
        task_id='tsk_consultar_api',
        python_callable=consultar_api,
        op_kwargs={"tipo": "diario"},
        owner='César',
    )

    tsk_verificar_json = BranchPythonOperator(
        task_id="tsk_verificar_json",
        python_callable=verificar_json_vazio,
        owner='César',
    )

    tsk_notificar_vazio = PythonOperator(
        task_id="tsk_notificar_vazio",
        python_callable=notificar_json_vazio,
        owner='César',
    )

    tsk_json_to_parquet = PythonOperator(
        task_id='tsk_json_to_parquet',
        python_callable=json_to_parquet,
        outlets=[Dataset(f'{PATH_DATASETS}raw_TorreTransacoes.parquet')],
        owner='César',
    )

    dag_sources_to_raw = TriggerDagRunOperator(
        task_id = "dag_sources_to_raw",
        trigger_dag_id="LoadSourcesToRaw",
        wait_for_completion=False,
        conf = {
            "filename": "TorreTransacoes",
            "identificador": "Transacao",
        },
        owner='César',
    )

    tsk_gerar_token >> tsk_consultar_api >> tsk_verificar_json
    tsk_verificar_json >> tsk_json_to_parquet >> dag_sources_to_raw
    tsk_verificar_json >> tsk_notificar_vazio