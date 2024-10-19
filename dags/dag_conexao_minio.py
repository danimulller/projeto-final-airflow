from airflow import DAG
from airflow.operators.python import PythonOperator  # Updated import statement
from datetime import datetime
from utils.minio_connect import MinioConnect

# Função para baixar o arquivo do MinIO
def print_json(**kwargs):  # Add **kwargs to pass execution context
    data_atual = datetime.now()

    ano = data_atual.year
    mes = data_atual.month
    dia = data_atual.day
    hora = data_atual.hour

    # Chame o método de MinioConnect corretamente
    arquivo = MinioConnect.get_file('raw', f'posicao/{ano}/{mes}/{dia}/{hora}/034dd864-e8b7-43fa-8fb2-0e6bb5723dbc.json')

    print(arquivo)

# Definição da DAG
with DAG(
    dag_id='minio_download_dag',
    start_date=datetime(2024, 8, 1),
    end_date=datetime(2024, 8, 6),
    schedule_interval="@daily",
    catchup=False  # Adiciona esta opção para evitar execuções passadas
) as dag:
    
    download_task = PythonOperator(
        task_id='download_file',
        python_callable=print_json  # Remove os parênteses para passar a função
    )

    download_task