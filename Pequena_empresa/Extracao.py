import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def create_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        print("Conexão bem-sucedida ao banco de dados PostgreSQL")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

conn = create_db_connection()

create_db_connection()

PASSWORD_ESCAPED = quote_plus(DB_PASSWORD)

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{PASSWORD_ESCAPED}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

tabela_dim_cliente = pd.read_sql_query(
    "SELECT * FROM stagin.contas_a_receber",
    conn
)

tabela_dim_cliente.to_sql(
    'contas_a_receber',
    engine,
    schema='dw',
    if_exists='replace',
    index=False
)


print("Tabela contas_a_receber transferida para o schema dw com sucesso.")
