'''
cli.py
Command line interface for travis to run tests
'''

import argparse

parser = argparse.ArgumentParser(description = "Enter name of sample to run paired end metagenomics pipeline")
parser.add_argument("-s", "--sample")
args = parser.parse_args()

def main(args=args):
    pass