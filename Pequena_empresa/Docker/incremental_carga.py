import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

USER = os.getenv("user", "postgres")
PASSWORD = os.getenv("password", "")
HOST = os.getenv("host", "localhost")
PORT = os.getenv("port", "5432")
DBNAME = os.getenv("dbname", "postgres")


def obter_engine():
    url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    return create_engine(url)


def _log(context, message, emoji="ℹ️"):
    formatted_message = f"{emoji} {message}"
    if context is not None:
        context.log.info(formatted_message)
    else:
        print(formatted_message)


def _resultado_para_dataframe(resultado):
    cabecalho = list(resultado.keys())
    return pd.DataFrame(resultado.fetchall(), columns=cabecalho)


def executar_etl(context=None):
    engine = obter_engine()
    ultima_quantidade = 0

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw"))

    tabelas_dimensao = {
        "clientes": "dim_clientes",
        "produtos": "dim_produtos",
        "vendedores": "dim_vendedores",
        "vendas": "fato_vendas",
    }

    _log(context, "Iniciando processo ETL de Carga Incremental...", emoji="🚀")

    for origem, destino in tabelas_dimensao.items():
        with engine.begin() as conn:
            if origem != "vendas":
                resultado = conn.execute(text(f"SELECT * FROM public.{origem}"))
                df = _resultado_para_dataframe(resultado)
                df["data_carga"] = pd.Timestamp.now()
                df.to_sql(destino, con=engine, if_exists="replace", index=False, schema="dw")
                _log(context, f"Dimensão 'dw.{destino}' sincronizada com sucesso! (Total de registros: {len(df)})", emoji="🔄")
            else:
                ultima_data = conn.execute(
                    text("SELECT MAX(data_venda) FROM dw.fato_vendas")
                ).fetchone()[0]

                if ultima_data:
                    query = f"SELECT * FROM public.{origem} WHERE data_venda > '{ultima_data}'"
                    _log(context, f"Buscando novos registros de vendas posteriores a {ultima_data}", emoji="🔍")
                else:
                    query = f"SELECT * FROM public.{origem}"
                    _log(context, "Iniciando Carga Inicial completa para fato_vendas", emoji="📥")

                resultado = conn.execute(text(query))
                df = _resultado_para_dataframe(resultado)
                df["data_carga"] = pd.Timestamp.now()
                df = df.drop(columns=["valor_unitario", "valor_total"], errors="ignore")
                ultima_quantidade = len(df)

                if not df.empty:
                    df.to_sql(destino, con=engine, if_exists="append", index=False, schema="dw")
                    _log(context, f"Inseridos {ultima_quantidade} novos registros de vendas em 'dw.{destino}'", emoji="📥")
                else:
                    _log(context, "Nenhum registro novo de vendas encontrado para inserir", emoji="✨")

                _log(context, f"Tabela de fatos 'dw.{destino}' atualizada incrementalmente com sucesso!", emoji="✅")

    _log(context, "Processo ETL finalizado com sucesso!", emoji="🎉")

    return {"novas_linhas": ultima_quantidade}


if __name__ == "__main__":
    executar_etl()
