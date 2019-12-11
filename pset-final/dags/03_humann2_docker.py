'''
Metagenomics Docker
Docker based pipeline to run the humann2 metagenomics pipeline
'''

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.models import DAG
from datetime import datetime, timedelta
import os

# Basic arguemnts to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days = 1),
}

# Create the head dag
dag = DAG(
    dag_id='humann2_docker', 
    default_args=args,
    schedule_interval=None)

humann_cmd = 'sh -c \'humann2_config --update database_folders utility_mapping /humann2/utility_mapping && \
        humann2_config --update database_folders protein /humann2/uniref && \
        humann2_config --update database_folders nucleotide /humann2/chocophlan && \
        humann2 --input /output/CSM9X23N_R1_kneaddata_paired.fastq \
                --output /output \
                --threads 1 \
                --search-mode uniref90 && \
        humann2_renorm_table --input /output/CSM9X23N_R1_kneaddata_paired_genefamilies.tsv --output /output/CSM9X23N_R1_kneaddata_paired_genefamilies_relab.tsv --units relab && \
        humann2_renorm_table --input /output/CSM9X23N_R1_kneaddata_paired_pathabundance.tsv --output /output/CSM9X23N_R1_kneaddata_paired_pathabundance_relab.tsv --units relab\''

humann2 = DockerOperator(
        task_id = 'humann2',
        image = 'biobakery/humann2:2.8.0',
        api_version = 'auto',
        volumes = ['/home/ubuntu/output:/input', '/home/ubuntu/output:/output', '/home/ubuntu/humann2:/humann2'],
        command = humann_cmd,
        docker_url = 'unix://var/run/docker.sock',
        network_mode = 'bridge',
        dag = dag
        )

# Define upload function
def upload(**kwargs):
    s3 = S3Hook()
    files = os.listdir('/home/ubuntu/output/')
    [s3.load_file('/home/ubuntu/output/' + file_name, 'output/' + file_name, bucket_name = 'airflow-project') for file_name in files]

upload_task = PythonOperator(
        python_callable = upload,
        task_id = "upload_to_s3",
        dag = dag
        )

humann2 >> upload_task
