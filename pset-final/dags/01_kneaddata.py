'''
01 - KneadData.py
DAG to run kneaddata(data cleaner) locally for testing purposes
'''

from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta

# Basic arguemnts to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days = 1),
}

# Create the head dag
dag = DAG(
    dag_id='kneaddata', 
    default_args=args,
    schedule_interval=None)

kneaddata = BashOperator(
    task_id='kneading', 
    bash_command='kneaddata -i /home/ubuntu/project_data/microbiome/HSM6XRUZ_R1.fastq.gz -i /home/ubuntu/project_data/microbiome/HSM6XRUZ_R2.fastq.gz -o /home/ubuntu/project_data/microbiome/output -db /home/ubuntu/microbiome/kneaddata', 
    dag=dag)
