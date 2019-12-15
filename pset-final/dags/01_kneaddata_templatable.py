'''
01 - KneadData Parameters.py
DAG to run kneaddata(data cleaner) locally for testing purposes with parameters
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
    dag_id='kneaddata_conf', 
    default_args=args,
    schedule_interval=None)

kneaddata = BashOperator(
    task_id='kneading', 
    bash_command='kneaddata -i {{ dag_run.conf["read1_dir"] }} -i {{ dag_run.conf["read2_dir"] }} -o {{ dag_run.conf["output_dir"] }} -db /isilon_biodata/dchen05/kneaddata --trimmomatic /bioinformatics/dchen05/applications/Trimmomatic-0.36/', 
    dag=dag)
