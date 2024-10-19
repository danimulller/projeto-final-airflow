# Laboratório Airflow

Este repositório é parte do projeto https://github.com/danimulller/projeto-final-bigdata.

## Inicializar o Ambiente

Para inicializar o serviço, utilize o comando:

```shell
docker compose -f docker/docker-compose.yml up --build
```

Usar `Ctrl+C` para parar a execução do ambiente

## Criar o Usuário para Fazer Login no Airflow

Após inicializar o serviço, crie um usuário admin para acessar a interface do Airflow:

1. Acesse o container do webserver:

```shell
docker compose -f docker/docker-compose.yml exec webserver bash
```

2. No container, crie o usuário admin:

```shell
airflow users create \
    --username admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## Configurar a Conexão Minio no Airflow

1. Acesse a interface do Airflow em [http://localhost:58080](http://localhost:58080) e faça login com as credenciais criadas.
2. Vá para `Admin` -> `Connections`.
3. Clique em `+` para adicionar uma nova conexão e configure os campos conforme abaixo:

- **Conn Id**: `minio_s3`
- **Conn Type**: `Amazon Web Services`
- **AWS Access Key ID**: `datalake`
- **AWS Secret Access Key**: `datalake`
- **Extra**: `{"endpoint_url": "http://localhost:9051"}`