from datetime import datetime

from dagster import (
    Definitions,
    MetadataValue,
    Output,
    asset,
    define_asset_job,
    ScheduleDefinition,
)
from incremental_carga import executar_etl


@asset(
    name="incremental_carga",
    group_name="pequena_empresa",
    description=(
        "Executa o processo de ETL incremental da Pequena Empresa. "
        "Carrega as dimensões (clientes, produtos, vendedores) e adiciona incrementalmente "
        "os novos registros de vendas ao DW."
    ),
)
def incremental_carga_asset(context) -> Output:
    """Executa o processo de ETL incremental e retorna informações úteis sobre a execução."""
    resultado = executar_etl(context)

    novas_linhas = resultado.get("novas_linhas", 0)
    data_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return Output(
        value=resultado,
        metadata={
            "novas_linhas_vendas": MetadataValue.int(novas_linhas),
            "tabelas_sincronizadas": MetadataValue.text(
                "clientes, produtos, vendedores, vendas"
            ),
            "data_ultima_execucao": MetadataValue.text(data_exec),
            "status_carga": MetadataValue.text(
                "Sucesso" if novas_linhas >= 0 else "Falha"
            ),
        },
    )


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
