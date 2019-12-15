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
    dag_id='upload_folder', 
    default_args=args,
    schedule_interval=None)


def upload(**kwargs):
    s3 = S3Hook()
    files = os.listdir('/home/ubuntu/output/')
    [s3.load_file('/home/ubuntu/output/' + file_name, 'output/' + file_name, bucket_name = 'airflow-project', replace = True) for file_name in files if not os.path.isdir('/home/ubuntu/output/' + file_name)]
    [s3.load_file('/home/ubuntu/output/CSM9X23N_R1_kneaddata_paired_humann2_temp/' + file_name, 'output/' + file_name, bucket_name = 'airflow-project', replace = True) for file_name in os.listdir('/home/ubuntu/output/CSM9X23N_R1_kneaddata_paired_humann2_temp')]

task = PythonOperator(
        python_callable = upload,
        task_id = "upload",
        dag = dag)
