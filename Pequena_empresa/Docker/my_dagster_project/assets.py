from dagster import (
    Definitions,
    asset,
    define_asset_job,
    ScheduleDefinition,
    Output,
    MetadataValue,
)

from incremental_carga import executar_etl


@asset(
    name="incremental_carga",
    description="Pipeline de ETL incremental que extrai dados do banco de dados transacional e atualiza as tabelas de dimensão (clientes, produtos, vendedores) e a tabela fato (vendas) no Data Warehouse (dw).",
    metadata={
        "author": "Equipe de Engenharia de Dados",
        "version": "1.1.0",
        "dw_schema": "dw",
        "source_tables": "clientes, produtos, vendedores, vendas",
        "target_tables": "dim_clientes, dim_produtos, dim_vendedores, fato_vendas",
    },
)
def incremental_carga_asset(context):
    res = executar_etl(context)
    novas_linhas = res.get("novas_linhas", 0)

    # Return output with rich runtime metadata for excellent developer/operator experience
    return Output(
        value=res,
        metadata={
            "novas_linhas_carregadas": MetadataValue.int(novas_linhas),
            "ultima_atualizacao": MetadataValue.text(pd_timestamp_now_str()),
            "status": MetadataValue.text("Sucesso 🎉"),
        },
    )


def pd_timestamp_now_str():
    import pandas as pd

    return str(pd.Timestamp.now())


incremental_carga_job = define_asset_job(
    name="incremental_carga_job",
    selection=[incremental_carga_asset],
)

incremental_carga_schedule = ScheduleDefinition(
    job=incremental_carga_job,
    cron_schedule="0 9 * * *",
    execution_timezone="America/Sao_Paulo",
)

defs = Definitions(
    assets=[incremental_carga_asset],
    jobs=[incremental_carga_job],
    schedules=[incremental_carga_schedule],
)
