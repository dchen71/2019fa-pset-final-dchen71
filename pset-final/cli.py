'''
cli.py
Command line interface for running metagenomics pipeline
'''

import argparse
import subprocess

parser = argparse.ArgumentParser(description = "Enter name of samples to run paired end metagenomics pipeline")
parser.add_argument("-s1", "--sample1")
parser.add_argument("-s2", "--sample2")
args = parser.parse_args()

def main(args=args):
    # Run subprocess to run bash process to call airflow and trigguer job
    subprocess_args = ["airflow", "trigger_dag", "metagenomics_docker", "--conf", "{\"read1_name\": \"" + args.sample1 + "\", \"read2_name\": \"" + args.sample2 + "\"}"]
    print(subprocess_args)
    subprocess.Popen(subprocess_args, shell = False)
