import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


sys.path.append('/opt/airflow/')
from scripts.etl_raw_to_bronze import extract_raw, transform_raw, load_bronze

tabelas = {
    "Fretes",
    "FretesAtores",
    "FretesConferencias",
    "FretesDinamico",
    "FretesExcluidos",
    "FretesFaturas",
    "FretesManifestos",
    "FretesOcorrencias"
}

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 17),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    'ETLRawtoBronze',
    tags=['ESL', 'API', 'Planejamento', 'ETL', 'Diário', 'Fretes', 'Sources'],
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

        tsk_extract_raw = PythonOperator(
            task_id=f'tsk_extract_raw',
            python_callable=extract_raw,
            owner='César',
            op_kwargs={"tabela": "{{ dag_run.conf.get('nome_relatorio', '') }}"}
        )

        tsk_transform_raw = PythonOperator(
            task_id=f'tsk_transform_raw',
            python_callable=transform_raw,
            owner='César',
            op_kwargs={"tabela": "{{ dag_run.conf.get('nome_relatorio', '') }}"}
        )

        tsk_load_bronze = PythonOperator(
            task_id=f'tsk_load_bronze',
            python_callable=load_bronze,
            owner='César',
            op_kwargs={"tabela": "{{ dag_run.conf.get('nome_relatorio', '') }}"}
        )

        tsk_extract_raw >> tsk_transform_raw >> tsk_load_bronze
        