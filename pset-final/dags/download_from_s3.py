'''
Test downloading to s3
Testing the downloading portion of s3hook
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
    dag_id='download', 
    default_args=args,
    schedule_interval=None)

def download(**kwargs):
    s3 = S3Hook()
    obj = s3.get_key('dinosaur.txt',
                     bucket_name = 'airflow-project')
    obj.download_file('/home/ubuntu/dinosaur.txt')

task = PythonOperator(
        python_callable = download,
        task_id = "download",
        dag = dag)
