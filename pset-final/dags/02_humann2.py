'''
02 - Humann2.py
DAG to run humann2(poop analyzer) locally for testing purposes
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
    dag_id='humann2', 
    default_args=args,
    schedule_interval=None)

humann_cmd = 'humann2_config --update database_folders utility_mapping /isilon_biodata/dchen05/humann2/utility_mapping && \
        humann2_config --update database_folders protein /isilon_biodata/dchen05/humann2/uniref && \
        humann2_config --update database_folders nucleotide /isilon_biodata/dchen05/humann2/chocophlan && \
        humann2 --input $sample \
                --output /bioinformatics/dchen05/testing/output \
                --threads $processors \
                --search-mode uniref90 && \
        humann2_renorm_table --input /bioinformatics/dchen05/testing/output/${sample_prefix}_genefamilies.tsv --output /bioinformatics/dchen05/testing/output/${sample_prefix}_genefamilies_relab.tsv --units relab && \
        humann2_renorm_table --input /bioinformatics/dchen05/testing/output/${sample_prefix}_pathabundance.tsv --output /bioinformatics/dchen05/testing/output/${sample_prefix}_pathabundance_relab.tsv --units relab'

humann2 = BashOperator(
    task_id='analyzer', 
    bash_command=humann_cmd, 
    dag=dag)
