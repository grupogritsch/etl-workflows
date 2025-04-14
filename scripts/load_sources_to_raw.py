import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable

PATH_DATASETS = Variable.get("PATH_DATASETS")

def parquet_to_raw(filename, identificador):
    """Insere os dados do parquet no banco de dados PostgreSQL."""
    arquivo_parquet = f'{PATH_DATASETS}Raw_{filename}.parquet'
    if not arquivo_parquet:
        raise ValueError("Nenhum arquivo parquet foi encontrado no XCom.")
    try:
        df = pd.read_parquet(arquivo_parquet, engine='pyarrow')
        df = df.where(pd.notna(df), None)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo parquet: {e}")
    if df.empty:
        print("Nenhum dado encontrado no arquivo parquet para inserir.")
        return
    postgres_hook = PostgresHook(postgres_conn_id="LakehouseRaw")
    engine = postgres_hook.get_sqlalchemy_engine()
    colunas = ", ".join([f'"{col}"' for col in df.columns])
    valores = ", ".join([f"%({col})s" for col in df.columns])
    update_set_str = ", ".join([f'"{col}" = EXCLUDED."{col}"' for col in df.columns if col != identificador])
    insert_query = f'''
    INSERT INTO "{filename}" ({colunas})
    VALUES ({valores})
    ON CONFLICT ("{identificador}") DO UPDATE 
    SET {update_set_str};
    '''
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_query, row.to_dict())
    print(f"Inserção concluída para a tabela {filename}. Linhas duplicadas foram atualizadas.")
