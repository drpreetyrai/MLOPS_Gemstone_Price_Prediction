from asyncio import tasks 
import json 
from textwrap import dedent 
import pendulum 
import sensor.pipeline.batch_prediction
import os 
from airflow import DAG 
from airflow.operators.python import PythonOperator 

import sys
sys.path.append('/path/to/your/sensor/package')  # Update this path to the actual location of the 'sensor' package

with DAG(
    'batch_prediction',
    default_args={'retries': 2},
    description='gemstone batch prediction',
    schedule_interval='@weekly', # you can also schedule based on hour and minutes 
    start_date=pendulum.datetime(2023, 10, 1, tz="UTC"),
    catchup=False,
    tags=['example'] 
) as dag: 
    def download_files(**kwargs):
        bucket_name=os.getenv("BUCKET_NAME") 
        input_dir = "/app/input_files" 
        os.makedirs(input_dir, exist_ok=True) 
        os.system(f"aws s3 cp s3://{bucket_name}/input_files {input_dir}") 

    def batch_prediction(**kwargs):
        from sensor.pipeline.batch_prediction import SensorBatchPrediction, BatchPredictionConfig   
        config = BatchPredictionConfig() 
        sensor_path_prediction = SensorBatchPrediction(config) 
        sensor_path_prediction.start_prediction()

    def upload_files(**kwargs):
        bucket_name=os.getenv("BUCKET_NAME") 
        os.system(f"aws s3 cp {config.archive_dir} s3://{bucket_name}/archive")
        os.system(f"aws s3 cp {config.outbox_dir} s3://{bucket_name}/outbox") 

    download_input_files = PythonOperator(
        task_id='download_input_files',
        python_callable=download_files,
        
    )

    generate_prediction = PythonOperator(
        task_id='prediction',
        python_callable=batch_prediction,
        
    )

    upload_prediction = PythonOperator(
        task_id='upload_prediction',
        python_callable=upload_files,
        
    )
    download_input_files >> generate_prediction >> upload_prediction

