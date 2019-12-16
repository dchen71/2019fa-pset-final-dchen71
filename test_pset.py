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

class DownloadTestCase(TestCase):
    ''' Test cases for airflow to download data for processing

    '''
    @mock_s3
    def test_DownloadRead(self):
        ''' Ensure that a file is downloaded '''
        conn = boto3.client('s3', region_name = 'us-west-1')
        conn.create_bucket(Bucket = "airflow-project") # Create virtual bucket
        conn.put_object(Bucket='airflow-project', Key= 'microbiome/testing_R1.fastq.gz', Body='') # Fill virtual bucket
        conn.download_file('airflow-project','microbiome/testing_R1.fastq.gz', 'data/testing_R1.fastq.gz')
        self.assertEqual(os.path.exists('data/testing_R1.fastq.gz'), True)




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
