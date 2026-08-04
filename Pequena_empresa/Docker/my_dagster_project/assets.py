from dagster import Definitions, asset, define_asset_job, ScheduleDefinition, Output, MetadataValue

from incremental_carga import executar_etl


@asset(
    name="incremental_carga",
    description="Ativo de dados responsável pelo processo de ETL incremental carregando dados das tabelas de clientes, produtos, vendedores e vendas do banco transacional para o Data Warehouse (dw).",
)
def incremental_carga_asset(context):
    resultado = executar_etl(context)
    novas_linhas = resultado.get("novas_linhas", 0)

    # Retorna o resultado com metadados detalhados para exibição elegante na UI do Dagster
    return Output(
        value=resultado,
        metadata={
            "novas_linhas_vendas": MetadataValue.int(novas_linhas),
            "schema_destino": MetadataValue.text("dw"),
            "dimensoes_atualizadas": MetadataValue.json(["dim_clientes", "dim_produtos", "dim_vendedores"]),
            "tabela_fato_atualizada": MetadataValue.text("fato_vendas"),
            "status_processamento": MetadataValue.text("Sucesso ✅"),
        }
    )


incremental_carga_job = define_asset_job(
    name="incremental_carga_job",
    selection=[incremental_carga_asset],
    description="Job que orquestra a execução do ativo de carga incremental ETL.",
)

incremental_carga_schedule = ScheduleDefinition(
    job=incremental_carga_job,
    cron_schedule="0 9 * * *",
    execution_timezone="America/Sao_Paulo",
    description="Agendamento diário às 09:00 (America/Sao_Paulo) para sincronização e carga incremental.",
)

defs = Definitions(
    assets=[incremental_carga_asset],
    jobs=[incremental_carga_job],
    schedules=[incremental_carga_schedule],
)
