import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

USER = os.getenv("user", "postgres")
PASSWORD = os.getenv("password", "")
HOST = os.getenv("host", "localhost")
PORT = os.getenv("port", "5432")
DBNAME = os.getenv("dbname", "postgres")


def obter_engine():
    url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    return create_engine(url)


def _log(context, message, level="info"):
    # Using eye-catching emojis and styling for great operator & developer UX
    if context is not None:
        if level == "info":
            context.log.info(message)
        elif level == "warning":
            context.log.warning(message)
        elif level == "error":
            context.log.error(message)
    else:
        prefix = "✨ "
        if level == "warning":
            prefix = "⚠️ "
        elif level == "error":
            prefix = "❌ "
        print(f"{prefix}{message}")


def _resultado_para_dataframe(resultado):
    cabecalho = list(resultado.keys())
    return pd.DataFrame(resultado.fetchall(), columns=cabecalho)


def executar_etl(context=None):
    _log(context, "===============================================")
    _log(context, "🚀 INICIANDO PIPELINE DE ETL INCREMENTAL 🚀")
    _log(context, "===============================================")

    engine = obter_engine()
    ultima_quantidade = 0

    with engine.begin() as conn:
        _log(context, "📁 Garantindo a existência do schema 'dw'...")
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw"))

    tabelas_dimensao = {
        "clientes": "dim_clientes",
        "produtos": "dim_produtos",
        "vendedores": "dim_vendedores",
        "vendas": "fato_vendas",
    }

    for origem, destino in tabelas_dimensao.items():
        with engine.begin() as conn:
            if origem != "vendas":
                _log(context, f"📥 Extraindo dados de origem: '{origem}'...")
                resultado = conn.execute(text(f"SELECT * FROM public.{origem}"))
                df = _resultado_para_dataframe(resultado)
                df["data_carga"] = pd.Timestamp.now()

                _log(context, f"📤 Carregando dimensão destino: 'dw.{destino}'...")
                df.to_sql(
                    destino, con=engine, if_exists="replace", index=False, schema="dw"
                )
                _log(
                    context,
                    f"✅ Dimensão '{destino}' atualizada com sucesso! ({len(df)} registros)",
                )
            else:
                _log(context, "🕒 Verificando última data na tabela de vendas...")
                # Check table existence safely using SQLAlchemy Inspector to avoid transaction abortion
                inspector = inspect(engine)
                tabela_existe = inspector.has_table("fato_vendas", schema="dw")

                ultima_data = None
                if tabela_existe:
                    try:
                        ultima_data = conn.execute(
                            text("SELECT MAX(data_venda) FROM dw.fato_vendas")
                        ).fetchone()[0]
                    except Exception:
                        _log(
                            context,
                            "⚠️ Falha ao obter última data de 'dw.fato_vendas'.",
                            level="warning",
                        )
                else:
                    _log(
                        context,
                        "⚠️ Tabela 'dw.fato_vendas' não encontrada no banco. Realizando carga inicial.",
                        level="warning",
                    )

                if ultima_data:
                    query = f"SELECT * FROM public.{origem} WHERE data_venda > '{ultima_data}'"
                    _log(
                        context,
                        f"🔄 Buscando dados incrementais desde {ultima_data}...",
                    )
                else:
                    query = f"SELECT * FROM public.{origem}"
                    _log(
                        context,
                        "📦 Nenhuma data anterior encontrada. Iniciando carga completa de vendas...",
                    )

                resultado = conn.execute(text(query))
                df = _resultado_para_dataframe(resultado)
                df["data_carga"] = pd.Timestamp.now()
                df = df.drop(columns=["valor_unitario", "valor_total"], errors="ignore")
                ultima_quantidade = len(df)

                if not df.empty:
                    _log(
                        context,
                        f"📤 Inserindo {ultima_quantidade} novos registros em 'dw.{destino}'...",
                    )
                    df.to_sql(
                        destino,
                        con=engine,
                        if_exists="append",
                        index=False,
                        schema="dw",
                    )
                    _log(context, f"✅ Tabela '{destino}' atualizada com sucesso!")
                else:
                    _log(
                        context, "💤 Nenhum dado novo para ser inserido na tabela fato."
                    )

    _log(context, "===============================================")
    _log(
        context, f"🎉 ETL CONCLUÍDO COM SUCESSO! ({ultima_quantidade} novas vendas) 🎉"
    )
    _log(context, "===============================================")

    return {"novas_linhas": ultima_quantidade}


if __name__ == "__main__":
    executar_etl()
