import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.append('/opt/airflow/')
from scripts.extract_sources_fretes import (
    baixar_arquivo,
    buscar_url_arquivo,
    retornar_datas,
    solicitar_relatorio,
    xlsx_to_parquet,
)

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 17),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    'ExtractSourcesFretes',
    tags=['ESL', 'API', 'Planejamento', 'Extração', 'Diário', 'Fretes', 'Sources'],
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    tsk_retornar_datas = PythonOperator(
        task_id='tsk_retornar_datas',
        python_callable=retornar_datas,
        owner='César',
    )

    tsk_solicitar_relatorio = PythonOperator(
        task_id='tsk_solicitar_relatorio',
        python_callable=solicitar_relatorio,
        op_kwargs={
            "id_relatorio": "{{ dag_run.conf.get('id_relatorio', '') }}",
            "filename": "{{ dag_run.conf.get('nome_relatorio', '') }}"
        },
        owner='César',
    )

    tsk_buscar_url_arquivo = PythonOperator(
        task_id="tsk_buscar_url_arquivo",
        python_callable=buscar_url_arquivo,
        owner='César',
    )

    tsk_baixar_arquivo = PythonOperator(
        task_id="tsk_baixar_arquivo",
        python_callable=baixar_arquivo,
        op_kwargs={"filename": "{{ dag_run.conf.get('nome_relatorio', '') }}"},
        owner='César',
    )

    tsk_xlsx_to_parquet = PythonOperator(
        task_id='tsk_xlsx_to_parquet',
        python_callable=xlsx_to_parquet,
        op_kwargs={"filename": "{{ dag_run.conf.get('nome_relatorio', '') }}"},
        outlets=[Dataset(f"{{ dag_run.conf.get('path_datasets', '') }}Raw_{{ dag_run.conf.get('nome_relatorio', '') }}.parquet")],
        owner='César',
    )

    dag_sources_to_raw = TriggerDagRunOperator(
        task_id = "dag_sources_to_raw",
        trigger_dag_id="LoadSourcesToRaw",
        wait_for_completion=True,
        conf = {
            "filename": "{{ dag_run.conf.get('nome_relatorio', '') }}",
            "identificador": "ID",
        },
        owner='César',
    )
    
    dag_raw_to_bronze = TriggerDagRunOperator(
        task_id=f'dag_raw_to_bronze',
        trigger_dag_id="ETLRawtoBronze",
        wait_for_completion=True,
        owner='César',
        conf={
            "nome_relatorio": "{{ dag_run.conf.get('nome_relatorio', '') }}"
        }
    )

    # Definição da ordem de execução
    tsk_retornar_datas >> tsk_solicitar_relatorio >> tsk_buscar_url_arquivo
    tsk_buscar_url_arquivo >> tsk_baixar_arquivo >> tsk_xlsx_to_parquet >> dag_sources_to_raw
    dag_sources_to_raw >> dag_raw_to_bronze

