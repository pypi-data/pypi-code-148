from 102003407 import topsis
import sys
import pandas as pd
import numpy as np
if len(sys.argv)!=5:
    print("Wrong command line input")
    exit()

topsis(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])