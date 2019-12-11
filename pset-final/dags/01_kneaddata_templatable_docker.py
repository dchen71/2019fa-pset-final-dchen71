'''
01 - KneadData Docker Templatable.py
DAG to run kneaddata(data cleaner) locally via docker for testing purposes with parameters
'''

from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from airflow.hooks.S3_hook import S3Hook
from datetime import datetime, timedelta

# Basic arguemnts to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days = 1),
}

# Create the head dag
dag = DAG(
    dag_id='kneaddata_docker', 
    default_args=args,
    schedule_interval=None)

# Create the S3 Downloader
def download(**kwargs):
    s3 = S3Hook()
    r1 = kwargs['dag_run'].conf.get('read1_name')
    r2 = kwargs['dag_run'].conf.get('read2_name')
    obj1 = s3.get_key('microbiome/' + r1,
                      bucket_name = 'airflow-project')
    obj1.download_file('/home/ubuntu/2019fa-pset-final-dchen71/data/' + r1)
    obj2 = s3.get_key('microbiome/' + r2,
                      bucket_name = 'airflow-project')
    obj2.download_file('/home/ubuntu/2019fa-pset-final-dchen71/data/' + r2)

downloader = PythonOperator(
        python_callable = download,
        provide_context = True,
        task_id = "download_data",
        dag = dag)

kneaddata = DockerOperator(
    task_id='kneading',
    image="biobakery/kneaddata:0.7.2",
    api_version='auto',
    volumes=['/home/ubuntu/2019fa-pset-final-dchen71/data:/input', '/home/ubuntu/output:/output', '/home/ubuntu/kneaddata:/db'],
    command='kneaddata -i /input/{{ dag_run.conf["read1_name"] }} -i /input/{{ dag_run.conf["read2_name"] }} -o /output -db /db', 
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    dag=dag)

filename = BashOperator(
        task_id='parse_filename',
        bash_command = "filename={{ dag_run.conf['read1_name'] }}; echo$(filename%%.*)",
        xcom_push = True,
        dag = dag
        )

downloader >> filename >> kneaddata
