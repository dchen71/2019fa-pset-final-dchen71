'''
02 - Merge Paried End.py
DAG to concatentate paired end reads for humann2
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
    dag_id='merge_paired_end_reads', 
    default_args=args,
    schedule_interval=None)

humann2 = BashOperator(
    task_id='pairer', 
    bash_command='cat /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired_1.fastq /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired_2.fastq > /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired.fastq', 
    dag=dag)
