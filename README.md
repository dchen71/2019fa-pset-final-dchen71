# Final - Airflow

[![Build Status](https://travis-ci.org/dchen71/2019fa-pset-final-dchen71.svg?branch=master)](https://travis-ci.org/dchen71/2019fa-pset-final-dchen71)
[![Maintainability](https://api.codeclimate.com/v1/badges/0c99d985d1da751173b0/maintainability)](https://codeclimate.com/github/dchen71/2019fa-pset-final-dchen71/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0c99d985d1da751173b0/test_coverage)](https://codeclimate.com/github/dchen71/2019fa-pset-final-dchen71/test_coverage)

## Introduction
In bioinformatics, our source of big data is comprised of the genetic makeup of animals, humans, bacteria, or any organism that can be sequenced from DNA into machine readable data into interpretable data. Depending on the type of test done on a person, the size of the datasets from a given patient can range from megabytes to gigabytes of data. In a whole experiment combined with many other individuals, a given experiment can potentially generate hundreds of gigabytes and even petabytes of data to process. This puts a strain on most traditional on premise ETL pipelines which relies on the typical and very limited high-performance clusters located on premise. Further compounding this issue, many algorithms are developed from academic institutions and offer varying levels of parallelization and multi-threading support. However, cloud solutions such as Amazon Web Services or Microsoft Azure can allow infinitely scalability of traditional bioinformatics workflows.  

The typical workflow depends on the type of experiment and data. On a high level, a typical workflow involves the processing of raw data sequencing data using various scripts downstream into data that is immediately usable for a bioinformatician. Many academic institutions use various workload managers such as Slurm, PBS, or any other job scheduler for local compute clusters for batch processing jobs. However, there are various issues with such HPC based solutions which renders it hard to use in a modern environment including docker support and many other issues. With the rise of cloud computing comes the rise of many job managers focused in managing cloud based pipelines.    

There are two popular workflow managers for batch processing of jobs currently. Apache Airflow was developed in AirBnB and is the most popular in terms of github stars. Luigi was developed in Spotify and would be a close second for most popular batch job workflow manager. Although both have different architectures, they both perform similar functions as a batch job workflow manager. They are both cloud native solutions which can leverage other technologies such as docker and kubernetes to infinitely scale.  

This repository is a proof of concept of the usability of Apache Airflow in the fields of bioinformatics. The pipeline developered here will be the realtively simple yet obscure metagenomics pipeline in the fields of the microbiome.  

## Methodology

### Apache Airflow
Apache airflow will be used to facilitate batch jobs. Apache Airflow has similar features to Luigi but appears to offer more flexibility to various tasks and functions as well as a nice UI to help visualize pipeline status.  

### Docker
Docker will be used in order to maintain package consistency. Specifically two docker images will be used, one for biobakery/kneaddata which preprocesses metagenomic data by removing human data and biobakery/humann2, which calculates relative abundance of bacterial species in stool samples. It is relatively simple to also setup the connection to pull from Amazon Elastic Container Registry for images to ensure images are not deleted off of dockerhub.  

#### KneadData
[Kneaddata Link](https://bitbucket.org/biobakery/kneaddata/wiki/Home)  
This algorithm cleans the raw data. This removes any human contaminant data so you should be left with only bacterial or viral data to feed downstream. Although technically this step is optional, it's better to run it to save time and cost and thus a requirement in this use case.  

Note: This requires a database which is not included in this repository to run.  

#### Humann2
[Humann2 Link](https://bitbucket.org/biobakery/humann2/wiki/Home)  
This algorithm has multiple functions. The first step is to quantify the relative abundance of how much bacteria is in the sample. From there, it calculates how much some of these species contribute to gene familes and metabolic pathway function.  

Note: This requires a large database which is not included in this repository to run.  

### Data
The data used in this project will be derived from the human microbiome project. This will be the raw metagenomic fastq files from fecal data specifically sourced from the Inflammatory Bowel Syndrome study. The raw WGS fastq data can be downloaded [here](https://portal.hmpdacc.org/search/s?filters=%7B%22op%22:%22and%22,%22content%22:%5B%7B%22op%22:%22in%22,%22content%22:%7B%22field%22:%22cases.sample_body_site%22,%22value%22:%5B%22feces%22%5D%7D%7D,%7B%22op%22:%22in%22,%22content%22:%7B%22field%22:%22cases.study_name%22,%22value%22:%5B%22IBDMDB%22%5D%7D%7D,%7B%22op%22:%22in%22,%22content%22:%7B%22field%22:%22files.file_format%22,%22value%22:%5B%22FASTQ%22%5D%7D%7D,%7B%22op%22:%22in%22,%22content%22:%7B%22field%22:%22files.file_type%22,%22value%22:%5B%22wgs_raw_seq_set%22%5D%7D%7D%5D%7D&facetTab=cases) but it is advised to download a few paired end samples for testing as the entire dataset is 2TB. For those not familiar with bioinformatic data in general, on a high level it is collecting DNA from somewhere and analyzing it in a sequencer machine to get raw chunks of DNA sequences. From these chunks of DNA sequences, we align them to a reference to figure out roughly how much of these chunks match a certain species for instance if it comes from a person. From there, there are more algorithms run based on the experiment to get more usable data for the downstream analyst.   

### AWS
This project is cloud focused as the original goal is to develop cloud centric technologies. Although ultimately not implemented, the goal was to set up Airflow with Kubernetes service via AWS EKS. This POC was built on a EC2 shuffling data between S3 in the same region to minimize cost and develop the framework to move towards Kuberentes and docker combined approach.    

## 
