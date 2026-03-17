import os
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from airflow.models import Variable
import re
import sys


load_dotenv()

def conectar_supabase():
    try:
        # Puxa do Airflow
        raw_url = Variable.get("supabase_url")
        raw_key = Variable.get("supabase_key")

        # LIMPEZA CRÍTICA: Remove espaços e aspas extras
        url = re.sub(r"['\"]", "", raw_url).strip()
        key = re.sub(r"['\"]", "", raw_key).strip()

        print(f"🔗 Tentando conectar em: {url[:25]}...")
        return create_client(url, key)
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        sys.exit(1) # Força o Airflow a mostrar que a Task falhou

def executar_etl_incremental_vendas():
    print("🚀 Iniciando ETL Incremental: Comparando IDs...")
    
    try:
        supabase = conectar_supabase()

        # 1. EXTRAÇÃO: Busca dados da tabela de origem (public.vendas)
        origem_res = supabase.table("vendas").select("*").execute()
        df_origem = pd.DataFrame(origem_res.data)
        
        if df_origem.empty:
            print("⚠️ Origem vazia.")
            return

        # 2. VERIFICAÇÃO: Busca os IDs que já estão no DW
        # Note que usamos .schema("dw") para acessar a tabela de destino
        dw_res = supabase.schema("dw").table("vendas").select("id_venda").execute()
        ids_no_dw = [item['id_venda'] for item in dw_res.data]

        # 3. FILTRAGEM: Somente IDs que NÃO estão no DW
        df_novos = df_origem[~df_origem['id_venda'].isin(ids_no_dw)].copy()

        if df_novos.empty:
            print("✨ Tudo em dia! Nenhum ID novo encontrado.")
            return

        # 4. TRANSFORMAÇÃO: Adiciona o timestamp de processamento
        # O formato ISO com f-string garante que o Supabase entenda o timestamptz
        df_novos['dw_processed_at'] = datetime.now().isoformat()

        print(f"🆕 Encontrados {len(df_novos)} novos registros para incluir.")

        # 5. CARGA: Insere os dados filtrados no DW
        registros_para_inserir = df_novos.to_dict(orient='records')
        supabase.schema("dw").table("vendas").insert(registros_para_inserir).execute()

        print(f"✅ Sucesso! {len(registros_para_inserir)} novas linhas inseridas no DW.")

    except Exception as e:
        print(f"❌ Erro no processo: {e}")

if __name__ == "__main__":
    executar_etl_incremental_vendas()