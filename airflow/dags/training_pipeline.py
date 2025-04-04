from __future__ import annotations 
import json 
from textwrap import dedent 
import pendulum 
from airflow import DAG 
from airflow.operators.python import PythonOperator 
from src.pipeline.training_pipeline import TrainingPipeline 
import numpy as np
import os 

training_pipeline=TrainingPipeline() 

with DAG(
    "gemstone_training_pipeline",
    default_args={"retries": 2},
    description="it is my training pipeline",
    schedule="@weekly",
    start_date=pendulum.datetime(2024, 3, 3, tz="UTC"),
    catchup=False,
    tags=['machine_learning','classification','gemstone'],
  ) as dag :

    dag.doc_md = __doc__  

    def data_ingestion(**kwargs):  
        ti = kwargs["ti"]
        train_data_path = test_data_path=training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", {"train_data_path": train_data_path} ) 

    def data_transformations(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact = ti.xcom_pull(task_ids="data_ingestion") 
        train_arr, test_arr = training_pipeline.data_transformation(data_ingestion_artifact) 
        train_arr = train_arr.tolist()
        test_arr = test_arr.tolist()
        ti.xcom_push("data_transformation_artifact", {"train_arr": train_arr, "test_arr": test_arr}) 

    def model_trainer(**kwargs):
        ti = kwargs["ti"]
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation") 
        train_arr = np.array(data_transformation_artifact["train_arr"]) 
        test_arr = np.array(data_transformation_artifact["test_arr"])
        model_trainer_artifact = training_pipeline.model_trainer(train_arr, test_arr) 
        ti.xcom_push("model_trainer_artifact", model_trainer_artifact)
    
    ## here you have to config azure blob 
    def push_data_to_s3(**kwargs):
        bucket_name = "repository_name"
        artifact_folder="/app/artifacts" 
        # you can save it to the azure blob 
        # os.system(f"aws s3 cp {artifact_folder} s3://{bucket_name}/artifacts")


    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
        
    )
    data_ingestion_task.doc_md = dedent(
        """
        ### Data Ingestion Task
        - This task ingests the data from the source and saves it to a specified location.
        - It uses the `TrainingPipeline` class to perform the ingestion.
        """
    )

    data_transform_task = PythonOperator(
        task_id="data_transformation",
        python_callable=data_transformations,
    )
    data_transform_task.doc_md = dedent(
        """
        ### Data Transformation Task
        - This task transforms the ingested data into a format suitable for training.
        - It uses the `TrainingPipeline` class to perform the transformation.
        """
    )


    model_trainer_task = PythonOperator(
        task_id="model_trainer",
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """
        ### Model Trainer Task
        - This task trains the model using the transformed data.
        - It uses the `TrainingPipeline` class to perform the training.
        """
    )

    push_data_to_s3_task = PythonOperator(
        task_id="push_data_to_s3",
        python_callable=push_data_to_s3,
    )
    push_data_to_s3_task.doc_md = dedent(
        """
        ### Push Data to S3 Task
        - This task pushes the artifacts to an S3 bucket.
        - It uses the AWS CLI to perform the upload.
        """
    )

    # Set task dependencies
    data_ingestion_task >> data_transform_task >> model_trainer_task >> push_data_to_s3_task
    # Set task dependencies


