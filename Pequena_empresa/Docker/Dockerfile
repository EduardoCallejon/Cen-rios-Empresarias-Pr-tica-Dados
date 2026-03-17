# 1. Definimos a imagem base (oficial do Airflow)
FROM apache/airflow:2.7.1

# 2. Copiamos o nosso arquivo de requisitos para dentro do container
COPY requirements.txt /requirements.txt

# 3. Instalamos as bibliotecas do requirements.txt
# Usamos o --no-cache-dir para manter a imagem leve
RUN pip install --no-cache-dir -r /requirements.txt