'''
01 - KneadData Docker Templatable.py
DAG to run kneaddata(data cleaner) locally via docker for testing purposes with parameters
'''

from airflow.operators.docker_operator import DockerOperator
from airflow.models import DAG
from datetime import datetime

# Basic arguemnts to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now(),
}

# Create the head dag
dag = DAG(
    dag_id='kneaddata_docker', 
    default_args=args,
    schedule_interval=None)

kneaddata = DockerOperator(
    task_id='kneading',
    image="biobakery/kneaddata:0.7.2",
    api_version='auto',
    volumes=['/bioinformatics/dchen05/testing:/input', '{{ dag_run.conf["output_dir"] }}:/output', '/isilon_biodata/dchen05/kneaddata:/db'],
    command='kneaddata -i /input/{{ dag_run.conf["read1_name"] }} -i /input/{{ dag_run.conf["read2_name"] }} -o /output -db /db', 
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    dag=dag)
