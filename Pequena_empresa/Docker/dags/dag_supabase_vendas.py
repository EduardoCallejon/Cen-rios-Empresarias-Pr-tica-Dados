from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configurações básicas da DAG
default_args = {
    'owner': 'eduardo',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_supabase_pme', # Nome que aparecerá na interface do Airflow
    default_args=default_args,
    description='ETL de Vendas: Supabase Public -> Supabase DW',
    schedule_interval=timedelta(days=1), # Roda 1 vez por dia
    start_date=datetime(2024, 1, 1),
    catchup=False, # Não tenta rodar datas passadas ao ligar
    tags=['consultoria', 'supabase'],
) as dag:

    # A tarefa que executa o script Python
    executar_etl = BashOperator(
        task_id='rodar_script_etl',
        bash_command='python /opt/airflow/scripts/etl_vendas.py',
    )

    executar_etl