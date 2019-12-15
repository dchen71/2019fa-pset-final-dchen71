'''
Test Uploading to s3
Testing the uploading portion of s3hook
'''

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.models import DAG
from datetime import datetime, timedelta
import os

# Basic arguments to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days = 1),
}

# Create the head dag
dag = DAG(
    dag_id='upload', 
    default_args=args,
    schedule_interval=None)

def upload(**kwargs):
    s3 = S3Hook()
    s3.load_file('/home/ubuntu/testing.txt',
                 'testing/testing.txt',
                  bucket_name = 'airflow-project')

task = PythonOperator(
        python_callable = upload,
        task_id = "upload",
        dag = dag)
