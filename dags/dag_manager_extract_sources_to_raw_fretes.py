from datetime import datetime, timedelta
from airflow.models import Variable
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import PythonOperator
import time

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 15, 3, 0),  # 15 de abril de 2025 às 03:00
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

def delay():
    time.sleep(3)

with DAG(
    'ManagerExtractSourcesFretes',
    tags=['ESL', 'API', 'Planejamento', 'Extração', 'Diário', 'Fretes', 'Manager'],
    default_args=default_args,
    schedule_interval='0 3 * * *',
    catchup=False,
) as dag:

    RAW_FRETES = Variable.get("raw_fretes_esl", deserialize_json=True)

    tsk_anterior = None

    for nome_relatorio, id_relatorio in RAW_FRETES:
        tsk_gatilho = TriggerDagRunOperator(
            task_id=f'dag_fretes_sources_{nome_relatorio}',
            trigger_dag_id="ExtractSourcesFretes",
            wait_for_completion=False,
            owner='César',
            conf={
                "nome_relatorio": nome_relatorio,
                "id_relatorio": id_relatorio
            }
        )

        tsk_delay = PythonOperator(
            task_id=f'tsk_delay_{nome_relatorio}',
            python_callable=delay,
            owner='César',
        )

        if  tsk_anterior:
            tsk_anterior >> tsk_gatilho
        tsk_gatilho >> tsk_delay
        tsk_anterior = tsk_delay
