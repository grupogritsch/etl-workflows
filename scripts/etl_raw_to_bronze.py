from airflow.providers.postgres.hooks.postgres import PostgresHook
import re
import pandas as pd
from datetime import datetime
from airflow.models import Variable

PATH_DATASETS = Variable.get("PATH_DATASETS")


def camel_to_snake(camel_str):
    snake_str = re.sub(r'([a-z])([A-Z])', r'\1_\2', camel_str)
    return snake_str.lower()

def extract_raw(tabela):
    # Criando a conexão com o banco de dados
    postgres_hook = PostgresHook(postgres_conn_id="LakehouseRaw")
    engine = postgres_hook.get_sqlalchemy_engine()

    # Definindo a query
    select_query = f'''
    SELECT * FROM "{tabela}"
    WHERE "Atualizacao"::DATE BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE;
    '''

    # Lendo os dados e armazenando em um DataFrame
    df = pd.read_sql(select_query, con=engine)
    df.to_parquet(f'{PATH_DATASETS}Bronze_{tabela}.parquet', engine='pyarrow', compression='snappy', index=False)

    return f'{PATH_DATASETS}Bronze_{tabela}.parquet'

def transform_raw(tabela):
    df = pd.read_parquet(f'{PATH_DATASETS}Bronze_{tabela}.parquet', engine='pyarrow')

    df.columns = [camel_to_snake(col) for col in df.columns]

    df.to_parquet(f'{PATH_DATASETS}Bronze_{tabela}.parquet', engine='pyarrow', compression='snappy', index=False)

def load_bronze(tabela):
    """Insere os dados do parquet no banco de dados PostgreSQL."""
    arquivo_parquet = f'{PATH_DATASETS}Bronze_{tabela}.parquet'
   
    if not arquivo_parquet:
        raise ValueError("Nenhum arquivo parquet foi encontrado.")
    
    try:
        df = pd.read_parquet(arquivo_parquet, engine='pyarrow')

    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo parquet: {e}")
    
    postgres_hook = PostgresHook(postgres_conn_id="LakehouseBronze")
    engine = postgres_hook.get_sqlalchemy_engine()
    
    colunas = ", ".join([f'{col}' for col in df.columns])
    valores = ", ".join([f"%({col})s" for col in df.columns])
    update_set_str = ", ".join([f'{col} = EXCLUDED.{col}' for col in df.columns if col != "id"])
    
    insert_query = f'''
    INSERT INTO {camel_to_snake(tabela)} ({colunas})
    VALUES ({valores})
    ON CONFLICT (id) DO UPDATE 
    SET {update_set_str};
    '''
    
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_query, row.to_dict())
    
    print(f"Inserção concluída para a tabela {tabela}. Linhas duplicadas foram atualizadas.")