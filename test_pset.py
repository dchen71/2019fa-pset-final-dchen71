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
        f = open('testing.txt', 'w+')
        f.close()
        conn.upload_file('testing.txt', 'airflow-project', 'testing.txt')
        os.remove("testing.txt")
        conn.download_file('airflow-project', 'testing.txt', 'testing.txt')
        self.assertEqual(os.path.exists('testing.txt'), True)





#class IntegrationTestCase(TestCase):
#    """ Basic Integration Tests """
#    dagbag = DagBag()
#    dag_id = pset_final.dags.metagenomics_docker
#    dag = dagbag.get_dag(dag_id)
#    args = dag.default_args
#
#    def test_dag_logic_and_syntax(self):
#        """Verify that there are no logical or syntactical errors in DAG.
#
#        Ideal response should return 0 errors (status == False).
#        """
#        assert not len(dagbag.import_errors)
