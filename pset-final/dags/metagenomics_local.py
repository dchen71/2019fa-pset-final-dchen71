'''
Metagenomics Local
Local pipeline to run the humann2 metagenomics pipeline
'''

from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from datetime import datetime
import os

# Basic arguemnts to pass to Airflow
args = {
    'owner': 'airflow',
    'start_date': datetime.now(),
}

# Create the head dag
dag = DAG(
    dag_id='metagenomics_local', 
    default_args=args,
    schedule_interval=None)

{% set input_dir = '/bioinformatics/dchen05/testing/' %}

# Run KneadData to preprocess the raw data 
kneaddata = BashOperator(
    task_id='kneaddata', 
    bash_command='kneaddata -i {{ input_dir + dag_run.conf["read1_name"] }} -i {{ input_dir + dag_run.conf["read2_name"] }} -o {{ dag_run.conf["output_dir"] }} -db /isilon_biodata/dchen05/kneaddata --trimmomatic /bioinformatics/dchen05/applications/Trimmomatic-0.36/', 
    dag=dag)

{% set base_name = os.path.splittext({{ dag_run.conf["read1_name"] }}) %}

# Concatenate the paired end reads
merge_reads = BashOperator(
    task_id='merge_paired_end_reads', 
    bash_command='cat {{ dat_run.conf["output_dir"]}}/{base_name}_kneaddata_paired_1.fastq {{ dat_run.conf["output_dir"]}}/{base_name}_R1_kneaddata_paired_2.fastq > {{ dat_run.conf["output_dir"]}}/{base_name}_kneaddata_paired.fastq', 
    dag=dag)

kneaddata >> merge_reads

# Run Hummann2 to find bacterial populations
humann_cmd = 'humann2_config --update database_folders utility_mapping /isilon_biodata/dchen05/humann2/utility_mapping && \
        humann2_config --update database_folders protein /isilon_biodata/dchen05/humann2/uniref && \
        humann2_config --update database_folders nucleotide /isilon_biodata/dchen05/humann2/chocophlan && \
        humann2 --input /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired.fastq \
                --output /bioinformatics/dchen05/testing/output \
                --threads 1 \
                --search-mode uniref90 && \
        humann2_renorm_table --input /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired_genefamilies.tsv --output /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired_genefamilies_relab.tsv --units relab && \
        humann2_renorm_table --input /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired_pathabundance.tsv --output /bioinformatics/dchen05/testing/output/HSM6XRUZ_R1_kneaddata_paired_pathabundance_relab.tsv --units relab'

humann2 = BashOperator(
    task_id='analyzer', 
    bash_command=humann_cmd, 
    dag=dag)

merge_reads >> humann2