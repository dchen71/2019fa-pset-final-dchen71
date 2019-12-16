#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_4.tasks` package."""


from unittest import TestCase
import os
import boto3
import mock
from moto import mock_s3


class DownloadTestCase(TestCase):
    ''' Test cases for airflow to download data for processing

    '''
    @mock_s3
    def test_DownloadRead(self):
        ''' Ensure that a file is downloaded '''
        conn = boto3.client('s3', region_name = 'us-west-1')
        conn.create_bucket(Bucket = "airflow-project") # Create virtual bucket
        conn.put_object(Bucket='airflow-project', Key= 'microbiome/testing_R1.fastq.gz', Body='') # Fill virtual bucket
        # maybe subprocess 
        # airflow test metagenomics_docker downloader testing_R1.fastq.gz
        self.assertEqual(os.path.exists('data/testing_R1.fastq.gz'), True)


