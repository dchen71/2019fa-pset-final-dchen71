'''
Test Passing Multi-parameters
Testing passing parameters downstream via xcoms
'''

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from datetime import datetime
import os

# Basic arguments to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now(),
}

# Create the head dag
dag = DAG(
    dag_id='test_multiparameters', 
    default_args=args,
    schedule_interval=None)

input_dir = '/bioinformatics/dchen05/dog/'

templated_command1 = """
touch /bioinformatics/dchen05/dog/{{ dag_run.conf['file_name'] }} ; filename={{ dag_run.conf['file_name'] }}; echo ${filename%%.*}
"""

# Touch data file 
touchy = BashOperator(
    task_id='create_data', 
    bash_command=templated_command1, 
    xcom_push = True,
    dag=dag)

cat_template = """
cat /bioinformatics/dchen05/dog/{{ti.xcom_pull(key = 'return_value')}}.fastq /bioinformatics/dchen05/dog/{{ti.xcom_pull(key = 'return_value')}}.fastq > /bioinformatics/dchen05/dog/{{ti.xcom_pull(key = 'return_value')}}.txt
"""

dacat = BashOperator(
    task_id="dacat",
    bash_command = cat_template,
    dag = dag
    )

touchy >> dacat
