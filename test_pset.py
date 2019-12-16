#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_4.tasks` package."""


from unittest import TestCase
import os
import boto3
import mock
from moto import mock_s3
from airflow.models import DagBag
import pset_final.dags.metagenomics_docker
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
import pytest
import datetime

class S3TestCase(TestCase):
    ''' Test cases for airflow to handle S3 pushing and pulling

    '''
    @mock_s3
    def test_DownloadRead(self):
        ''' Ensure that a file is downloaded '''
        conn = boto3.client('s3', region_name = 'us-west-1')
        conn.create_bucket(Bucket = "airflow-project") # Create virtual bucket
        conn.put_object(Bucket='airflow-project', Key= 'microbiome/testing_R1.fastq.gz', Body='') # Fill virtual bucket
        conn.download_file('airflow-project','microbiome/testing_R1.fastq.gz', 'data/testing_R1.fastq.gz')
        
        self.assertEqual(os.path.exists('data/testing_R1.fastq.gz'), True)

    @mock_s3
    def test_UploadRead(self):
        ''' Ensure that files can be pushed to S3 '''
        conn = boto3.client('s3', region_name = 'us-west-1')
        conn.create_bucket(Bucket = 'airflow-project')
        f = open('data/testing.txt', 'w+')
        f.close()
        conn.upload_file('data/testing.txt', 'airflow-project', 'testing.txt')
        os.remove("data/testing.txt")
        conn.download_file('airflow-project', 'testing.txt', 'data/testing.txt')
        
        self.assertEqual(os.path.exists('data/testing.txt'), True)



##
## Note
## Airflow unit tests all require running against a live server due to how it's built
## EIther need to run it against a detached docker image or run it against a locally running instance
##

@pytest.fixture
def test_dag():
    """ Base dag for testing """
    return DAG(
        "test_dag",
        default_args={"owner": "airflow", "start_date": datetime.datetime(2018, 1, 1)},
        schedule_interval=datetime.timedelta(days=1),
    )

pytest_plugins = ["helpers_namespace"]

@pytest.helpers.register
def run_task(task, dag):
    """ Base runner for dags """
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
        end_date=dag.default_args["start_date"],
    )


class TaskTestCase(TestCase):
    """ Basic tests for tasks """
    def merge_paired_end_reads(self):
        ''' Test the merge paired end reads task '''
        # Create dummy paired end reads
        f = open('output/f1_R1_kneaddata_paired_1.fastq', 'w+')
        f.write('dog')
        f.close()
        f = open('output/f1_R1_kneaddata_paired_2.fastq', 'w+')
        f.close()
        
        # Run the task
        task = BashOperator(task_id = "test", bash_command = "cat output/f1_R1_kneaddata_paired_1.fastq output/f1_R1_kneaddata_paired_2.fastq > output/f1_R1_kneaddata_paired.fastq", dag = test_dag)
        self.assertEqual(os.path.exists('output/f1_R1_kneaddata_paired.fastq'), True) # Check for combined file
        f = open('output/f1_R1_kneaddata_paired.fastq')
        self.assertEqual(f.read(), 'dog') # Check that it concatenated

    #@mock_s3
    #def test_downloader(self):
    #    ''' Test the downloading task '''
    #    def download(**kwargs):
    #        ''' Downloading s3 function '''
    #        s3 = S3Hook()
    #        file_list = ['testing_R1.fastq', 'testing_R2.fastq']
    #        [s3.get_key(os.path.join('microbiome', file_name), bucket_name = 'airflow-project').download_file(os.path.join(os.path.abspath('data'), file_name)) for file_name in file_list] # Get path from S3 and download locally

    #    # Init the dummy files
    #    conn = boto3.client('s3', region_name = 'us-west-1')
    #    conn.create_bucket(Bucket = 'airflow-project')
    #    conn.put_object(Bucket='airflow-project', Key = 'microbiome/testing_R1.fastq', Body = '')
    #    conn.put_object(Bucket='airflow-project', Key = 'microbiome/testing_R2.fastq', Body = '')
        
    #    # Run the test on the download function
    #    task = PythonOperator(task_id="test", python_callable=download, provide_context = True, dag=test_dag)
    #    pytest.helpers.run_task(task=task, dag=test_dag)
    #    self.assertEqual(os.path.exists('data/microbiome/testing_R1.fastq'), True) # Check that it downloaded
    #    self.assertEqual(os.path.exists('data/microbiome/testing_R2.fastq'), True) # Check that it downloaded

class IntegrationTestCase(TestCase):
    """ Basic Integration Tests """

    def test_dag_for_errors(self):
        """Verify that there are no logical or syntactical errors in DAG.

        Ideal response should return 0 errors (status == False).
        AKA make sure this thing has working dags
        """
        dagbag = DagBag()
        self.assertEqual(len(dagbag.import_errors), 0) # Check that it can import dags okay


