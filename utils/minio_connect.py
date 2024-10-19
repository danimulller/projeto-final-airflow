from airflow.providers.amazon.aws.hooks.s3 import S3Hook

class MinioConnect:
    def __init__(self, client):
        self.client = client  # Assume 'client' is an instance of Minio or similar

    def get_file(self, bucket_name: str = 'raw', file_path: str = ''):
        try:
            hook = S3Hook(aws_conn_id='minio_s3')  # Reference to the connection created in Airflow
            
            # Download the file
            file_content = hook.read_key(key=file_path, bucket_name=bucket_name)

            return file_content  # Return the file content
        except Exception as e:
            print(f"An error occurred while getting the file from MinIO: {e}")
            return False  # Return False if an error occurs