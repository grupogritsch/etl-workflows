import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append('/opt/airflow/')
from scripts.load_sources_to_raw import parquet_to_raw

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 17),
    #'email': ['planejamento@gritsch.com.br'],
    #'email_on_failure': True,
    #'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    'LoadSourcesToRaw',
    tags=['Carregar', 'RAW', 'PostgreSQL', 'Diário'],
    default_args = default_args,
    schedule_interval = None,
    catchup = False,
) as dag:
    
    tsk_sources_to_raw = PythonOperator(
        task_id='tsk_sources_to_raw',
        python_callable=parquet_to_raw,
        op_kwargs={
            "filename": "{{ dag_run.conf.get('filename', '') }}",
            "identificador": "{{ dag_run.conf.get('identificador', '') }}"            
        },
        owner='César',
    )

    tsk_sources_to_raw
    