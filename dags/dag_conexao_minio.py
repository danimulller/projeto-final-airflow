from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Defina o bucket e a pasta onde estão os JSONs
BUCKET_NAME = 'raw'
PREFIX = 'posicao/2024/10/21/19/'

# Função para obter o último arquivo JSON da pasta
def get_latest_json(**kwargs):
    s3_hook = S3Hook(aws_conn_id='minio_s3')  # 'minio_s3' é o ID da conexão no Airflow
    bucket_keys = s3_hook.list_keys(bucket_name=BUCKET_NAME, prefix=PREFIX)
    
    # Filtrar apenas arquivos JSON
    json_files = [key for key in bucket_keys if key.endswith('.json')]
    
    if not json_files:
        raise ValueError('Nenhum arquivo JSON encontrado.')
    
    # Ordenar os arquivos pela data de modificação
    json_files.sort(key=lambda key: s3_hook.get_key(key, bucket_name=BUCKET_NAME).last_modified, reverse=True)
    
    # O último arquivo será o mais recente
    latest_file = json_files[0]
    
    # Retornar o conteúdo do arquivo
    file_content = s3_hook.read_key(latest_file, bucket_name=BUCKET_NAME)
    print(f'O último arquivo JSON é: {latest_file}')
    print(f'Conteúdo: {file_content}')
    return latest_file

# Definir o DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 0
}

with DAG(
    'get_latest_json',
    default_args=default_args,
    description='Um DAG para coletar o último JSON da pasta posicao no MinIO',
    schedule_interval=None,
) as dag:

    # Operador Python para coletar o último JSON
    get_json_task = PythonOperator(
        task_id='get_latest_json_task',
        python_callable=get_latest_json,
        provide_context=True,
        dag=dag,
    )