import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine


def create_db_connection():

    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=users,
            password=password,
            port=
        )
        print("Conexão bem-sucedida ao banco de dados PostgreSQL")
    except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
    return conn

create_db_connection()





