import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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
        with engine.connect():
            print("🚀 Conexão com o banco de dados realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        print("\n💡 DICA DE SOLUÇÃO:")
        print(
            "   Por favor, certifique-se de que o arquivo `.env` existe no diretório 'Pequena_empresa/Docker/'"
        )
        print(
            "   e que contém as credenciais corretas ('user', 'password', 'host', 'port', 'dbname').\n"
        )
        raise e
    return engine


catalogo_tabelas = {
    "clientes": "dim_clientes",
    "produtos": "dim_produtos",
    "vendas": "fato_vendas",
    "vendedores": "dim_vendedores",
}

engine = conexao()

print("\n🚀 Iniciando a carga inicial de dados...")

for origem, destino in catalogo_tabelas.items():
    print(f"📥 Processando tabela de origem '{origem}' para '{destino}' no DW...")
    try:
        with engine.connect() as connection:
            resultado = connection.execute(text(f"SELECT * FROM {origem}"))
            cabecalho = [desc[0] for desc in resultado.cursor.description]
            df = pd.DataFrame(resultado.fetchall(), columns=cabecalho)
            df["data_carga"] = pd.Timestamp.now()
            if origem == "vendas":
                df = df.drop(columns=["valor_unitario", "valor_total"])
        df.to_sql(destino, con=engine, if_exists="replace", index=False, schema="dw")
        print(f"✅ Tabela '{destino}' carregada com sucesso ({len(df)} linhas)!")
    except Exception as e:
        print(f"❌ Erro ao carregar a tabela '{origem}' para '{destino}': {e}")
        raise e

print("\n✨ Carga de dados inicial concluída com sucesso!\n")
