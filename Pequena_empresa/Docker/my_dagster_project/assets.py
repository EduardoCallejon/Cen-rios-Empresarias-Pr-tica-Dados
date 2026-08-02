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
    description="Executa o pipeline de ETL incremental carregando dados transacionais e atualizando as dimensões no DW.",
)
def incremental_carga_asset(context):
    resultado = executar_etl(context)
    novas_linhas = (
        resultado.get("novas_linhas", 0) if isinstance(resultado, dict) else 0
    )
    return Output(
        value=resultado,
        metadata={
            "novas_linhas_carregadas": MetadataValue.int(novas_linhas),
            "status_execucao": MetadataValue.string("Sucesso"),
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
