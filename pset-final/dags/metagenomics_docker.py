'''
Metagenomics Docker
Docker based pipeline to run the humann2 metagenomics pipeline
Ex: airflow trigger_dag metagenomics_docker --conf '{"read1_name":"CSM_R1.fastq", "read2_name":"CSM_R2.fastq"}'
'''

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.models import DAG
from datetime import datetime, timedelta
import os

# Basic arguments to pass to Airflow for initialization
args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days = 1),
}

# Create the head dag
dag = DAG(
    dag_id='metagenomics_docker', 
    default_args=args,
    schedule_interval=None)

# Create the S3 download function
def download(**kwargs):
    s3 = S3Hook()
    file_list = [kwargs['dag_run'].conf.get(read) for read in ['read1_name', 'read2_name']] # Pull conf names
    [s3.get_key(os.path.join('microbiome', file_name), bucket_name = 'airflow-project').download_file(os.path.join(os.path.abspath('data'), file_name)) for file_name in file_list] # Get path from S3 and download locally

# Downloader Operator
downloader = PythonOperator(
        python_callable = download,
        provide_context = True,
        task_id = "download_data",
        dag = dag)

# Parse filename
filename = BashOperator(
        task_id = 'parse_filename',
        bash_command = "filename={{ dag_run.conf['read1_name'] }}; echo ${filename%%.*}",
        xcom_push = True,
        dag = dag
        )

# Run KneadData to preprocess data
kneaddata = DockerOperator(
        task_id = 'kneaddata',
        image = 'biobakery/kneaddata:0.7.2',
        api_version = 'auto',
        volumes = ['/home/ubuntu/2019fa-pset-final-dchen71/data:/input', '/home/ubuntu/output:/output', '/home/ubuntu/kneaddata:/db'],
        command = 'kneaddata -i /input/{{ dag_run.conf["read1_name"] }} -i /input/{{ dag_run.conf["read2_name"] }} -o /output -db /db',
        docker_url = 'unix://var/run/docker.sock',
        network_mode = 'bridge',
        dag = dag
        )


# Concatenate the paired end reads
merge_reads = BashOperator(
    task_id='merge_paired_end_reads', 
    bash_command="cat /home/ubuntu/output/{{ti.xcom_pull(key = 'return_value')}}_kneaddata_paired_1.fastq /home/ubuntu/output/{{ti.xcom_pull(key = 'return_value')}}_kneaddata_paired_2.fastq > /home/ubuntu/output/{{ti.xcom_pull(key = 'return_value')}}_kneaddata_paired.fastq", 
    dag=dag)


# Run Hummann2 to find bacterial populations
humann_cmd = 'sh -c \'humann2_config --update database_folders utility_mapping /humann2/utility_mapping && \
        humann2_config --update database_folders protein /humann2/uniref && \
        humann2_config --update database_folders nucleotide /humann2/chocophlan && \
        humann2 --input /output/{{ti.xcom_pull(key = "return_value")}}_kneaddata_paired.fastq \
                --output /output \
                --threads 1 \
                --search-mode uniref90 && \
        humann2_renorm_table --input /output/{{ti.xcom_pull(key = "return_value")}}_kneaddata_paired_genefamilies.tsv --output /output/{{ti.xcom_pull(key = "return_value")}}_kneaddata_paired_genefamilies_relab.tsv --units relab && \
        humann2_renorm_table --input /output/{{ti.xcom_pull(key = "return_value")}}_kneaddata_paired_pathabundance.tsv --output /output/{{ti.xcom_pull(key = "return_value")}}_kneaddata_paired_pathabundance_relab.tsv --units relab\''

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
    file_base = kwargs['ti'].xcom_pull(task_ids = "parse_filename")
    [s3.load_file('/home/ubuntu/output/' + file_name, 'output/' + file_name, bucket_name = 'airflow-project', replace = True) for file_name in files if not os.path.isdir('/home/ubuntu/output/' + file_name)]
    [s3.load_file('/home/ubuntu/output/'+file_base+'_kneaddata_paired_humann2_temp/' + file_name, 'output/' + file_name, bucket_name = 'airflow-project', replace = True) for file_name in os.listdir('/home/ubuntu/output/'+file_base+'_kneaddata_paired_humann2_temp')]

upload_task = PythonOperator(
        python_callable = upload,
        task_id = "upload_to_s3",
        provide_context = True,
        dag = dag
        )

downloader >> filename >> kneaddata >> merge_reads >> humann2 >> upload_task
