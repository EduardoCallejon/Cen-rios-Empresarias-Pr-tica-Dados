from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd


# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def conexao():
    # Construct the SQLAlchemy connection string
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")
    return engine

catalogo_tabelas ={
    'clientes': 'dim_clientes',
    'produtos': 'dim_produtos',
    'vendas': 'fato_vendas',
    'vendedores': 'dim_vendedores'
}

engine = conexao()

for origem,destino in catalogo_tabelas.items():
        with engine.connect() as connection:
            resultado = connection.execute(text(f"SELECT * FROM {origem}"))
            cabecalho = [desc[0] for desc in resultado.cursor.description]
            df = pd.DataFrame(resultado.fetchall(), columns=cabecalho)
            df['data_carga'] = pd.Timestamp.now()
            if origem == 'vendas':
                df = df.drop(columns=['valor_unitario', 'valor_total'])
        df.to_sql(destino, con=engine, if_exists='replace', index=False, schema='dw')
        
print("Data loaded successfully!")