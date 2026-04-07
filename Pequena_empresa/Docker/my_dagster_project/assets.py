from dagster import Definitions, asset, define_asset_job, ScheduleDefinition

from incremental_carga import executar_etl


@asset(name="incremental_carga")
def incremental_carga_asset(context):
    return executar_etl(context)


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
