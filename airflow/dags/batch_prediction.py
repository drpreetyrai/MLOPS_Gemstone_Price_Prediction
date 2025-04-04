from asyncio import tasks 
import json 
from textwrap import dedent 
import pendulum 
import os 
from airflow import DAG 
from airflow.operators.python import PythonOperator 

with DAG(
    'batch_prediction',
    default_args={'retries': 2},
    description='gemstone batch prediction',
    schedule_interval='@weekly', 
    start_date=pendulum.datetime(2023, 10, 1, tz="UTC"),
    catchup=False,
    tags=['example'] 
) as dag: 

