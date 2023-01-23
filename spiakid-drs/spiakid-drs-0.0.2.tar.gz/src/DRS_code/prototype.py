#!/usr/bin/env python
#
import h5py
import sys
import numpy as np
import pandas as pd
import Functions.GUI as G
import argparse

def parse():
    # read in command line arguments
    parser = argparse.ArgumentParser(description='MKID Pipeline CLI')
    parser.add_argument('--init', action='store_true', help='Setup the pipeline, clobbers _default.yaml as needed')
    return parser.parse_args()



if __name__ == "__main__":
    args = parse()
    if args.init:
        G.interface()
        print('Hello')
        sys.exit(0)