'''
01 - KneadData.py
DAG to run kneaddata(data cleaner) locally for testing purposes
'''

from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from datetime import datetime

# Basic arguemnts to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now(),
}

# Create the head dag
dag = DAG(
    dag_id='kneaddata', 
    default_args=args,
    schedule_interval=None)

kneaddata = BashOperator(
    task_id='kneading', 
    bash_command='kneaddata', 
    dag=dag)
