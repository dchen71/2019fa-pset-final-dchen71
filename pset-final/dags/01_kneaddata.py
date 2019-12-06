'''
01 - KneadData.py
DAG to run kneaddata(data cleaner) locally for testing purposes
'''

from builtins import range
from airflow.operators import BashOperator, DummyOperator
from airflow.models import DAG
from datetime import datetime, timedelta

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
