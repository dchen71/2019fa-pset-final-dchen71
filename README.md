# Final - Airflow

[![Build Status](https://travis-ci.org/dchen71/2019fa-pset-final-dchen71.svg?branch=master)](https://travis-ci.org/dchen71/2019fa-pset-final-dchen71)
[![Maintainability](https://api.codeclimate.com/v1/badges/0c99d985d1da751173b0/maintainability)](https://codeclimate.com/github/dchen71/2019fa-pset-final-dchen71/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0c99d985d1da751173b0/test_coverage)](https://codeclimate.com/github/dchen71/2019fa-pset-final-dchen71/test_coverage)

## Introduction
In bioinformatics, big data is comprised of the genetic makeup of animals, humans, bacteria, or any organism that can be sequenced from the machines into interpretable data. An individual’s raw data can be very small datasets in the megabyte size but can range common in the gigabyte size. Combined, a whole experiment can potentially generate hundreds of gigabytes and even petabytes of data to process. This puts a strain on most traditional analysis methodology which relies on the typical and very limited high-performance clusters located on premise. Further compounding this issue, many algorithms are developed from academic institutions and offer varying levels of parallelization and multi-threading support. Cloud solutions such as Amazon Web Services or Microsoft Azure can allow infinitely scalability of traditional bioinformatics workflows.  

The typical workflow depends on the type of experiment and data, a typical workflow involves the processing of raw data using various scripts downstream into data that is immediately usable. Many academic institutions use various workload managers such as Slurm, PBS, or any other job scheduler for local compute clusters for batch processing jobs.  There are various issues with such HPC based solutions which renders it hard to use in a modern cloud environment including docker support and many other issues. There are numerous cloud native workflow managers which would be enough for moving existing HPC pipelines over to a cloud native one.  

There are two popular workflow managers for batch processing of jobs currently. Apache Airflow was developed in AirBnB and is the most popular in terms of github stars. Luigi was developed in Spotify and would be a close second for most popular batch job workflow manager. Although both have different architectures, they both perform similar functions as a batch job workflow manager. They are both cloud native solutions which can leverage other technologies such as kubernetes to infinitely scale.  

This repository is a proof of concept of the usability of Apache Airflow in the fields of bioinformatics. The pipelines used will be the realtively simple yet obscure metagenomics pipeline.  

## Methodology

### Apache Airflow
Apache airflow will be used to facilitate batch jobs. Apache Airflow has similar features to Luigi but appears to offer more flexibility to various tasks and functions as well as a nice UI to help visualize pipeline status.  

### Docker
Docker will be used in order to maintain package consistency. Specifically two docker images will be used, one for biobakery/kneaddata which preprocesses metagenomic data by removing human data and biobakery/humann2, which calculates relative abundance of bacterial species in stool samples.

### Data
The data used in this project will be derived from the human microbiome project. This will be the raw metagenomic fastq files from fecal data.
