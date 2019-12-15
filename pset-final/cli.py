'''
cli.py
Command line interface for travis to run tests
'''

import argparse
import subprocess

parser = argparse.ArgumentParser(description = "Enter name of sample to run paired end metagenomics pipeline")
parser.add_argument("-s1", "--sample1")
parser.add_argument("-s2", "--sample2")
args = parser.parse_args()

def main(args=args):
    subprocess.Popen(["airflow", "trigger_dag", "metagenomics_docker", "--conf", "{\"read_1\": \"" + args.sample1 + "\", \"read2_name\": \"" + args.sample2 + "\"}"])
