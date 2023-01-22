# Code to Implement TOPSIS
# Importing the required libraries
import sys
import pandas as pd
import numpy as np
import argparse

def validate_data(input_file, weights, impacts):
    """
    Validate the input data.
    """

    # Handling of “File not Found” exception
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(1)

    # Input file must contain three or more columns.
    if len(df.columns) < 3:
        print("Error : Input file must contain three or more columns")
        sys.exit(1)

    #Checking if the weights are numeric
    try: 
        weights = [float(i) for i in weights.split(',')]
    except ValueError:
        print("Error : Weights must be numeric")
        sys.exit(1)

    #Checking if the impacts are either +ve or -ve
    if not all(i == '+' or i == '-' for i in impacts.split(',')):
        print("Error : Impacts must be either +ve or -ve")
        sys.exit(1)
        
    # Weights must be positive 
    if not all(i > 0 for i in weights):
        print("Error : Weights must be positive")
        sys.exit(1)

    #Checking if the number of weights and impacts are equal to the number of columns
    try:
        if len(weights) != len(df.columns) - 1 or len(impacts.split(',')) != len(df.columns) - 1:
            print("Error : Number of weights and impacts must be equal to the number of columns")
            sys.exit(1)
    except ValueError: 
        print("Error : Number of weights and impacts must be equal to the number of columns")
        sys.exit(1)

    #Checking if impacts and weights are separated by comma
    try: 
        if ',' not in impacts or ',' not in weights:
            print("Error : Impacts and weights must be separated by comma")
            sys.exit(1)
    except ValueError:
        print("Error : Impacts and weights must be separated by comma")
        sys.exit(1)

    # From 2nd column onwards, columns must contain numeric values only (Handling of non-numeric values)
    for i in df.columns[1:]:
        try:
            df[i] = df[i].apply(lambda x: float(x))
        except ValueError:
            print("Error : From 2nd column onwards, columns must contain numeric values only")
            sys.exit(1)
    
    return df, weights, impacts


def normalize(df, ncols, weights):

    #Normalizing the data and calculating the weighted normalized data matrix
    for i in range(ncols):
        df.iloc[:,i+1] = df.iloc[:,i+1]/np.sqrt(sum(df.iloc[:,i+1]**2))
        df.iloc[:,i+1] = df.iloc[:,i+1]*weights[i]
    return df

def calculation(df, ncols, impacts):
    #Calculating the ideal values
    ideal_best = []
    ideal_worst = []
    for i in range(ncols):
        if impacts[i] == '+':
            ideal_best.append(max(df.iloc[:,i+1]))
            ideal_worst.append(min(df.iloc[:,i+1]))
        else:
            ideal_best.append(min(df.iloc[:,i+1]))
            ideal_worst.append(max(df.iloc[:,i+1]))

    #Calculating the euclidean distance from ideal best and ideal worst
    Si_best = []
    Si_worst = []
    for i in range(len(df)):
        Si_best.append(np.sqrt(np.sum(np.square(df.iloc[i,1:] - ideal_best))))
        Si_worst.append(np.sqrt(np.sum(np.square(df.iloc[i,1:] - ideal_worst))))
    df['euclidean_distance_best'] = Si_best
    df['euclidean_distance_worst'] = Si_worst
    
    return df, ideal_best, ideal_worst

def performance_score(df):
    #Calculating the performance score
    df['performance_score'] = df['euclidean_distance_worst']/(df['euclidean_distance_best'] + df['euclidean_distance_worst'])
    return df

def ranking(df):
    #Ranking the alternatives
    df['ranking'] = df['performance_score'].rank(ascending=False)
    return df

def topsis(input_file, weights, impacts, result_file):

    #Reading the input file
    df = pd.read_csv(input_file)
    df_raw = pd.read_csv(input_file)
    ncols = len(df.columns) - 1
    
    #Converting the weights and impacts to lists
    weights = weights.split(',')
    impacts = impacts.split(',')

    #Converting weight to floats
    weights = [float(i) for i in weights]

    #Normalizing the data
    df = normalize(df, ncols, weights)

    #Calculating the ideal values & Eucledian distance
    df, ideal_best, ideal_worst = calculation(df, ncols, impacts)

    #Calculating the performance score
    df = performance_score(df)

    #Ranking the alternatives
    df = ranking(df)

    #add the last two columns of df to df_raw
    df_raw['performance_score'] = df['performance_score']
    df_raw['ranking'] = df['ranking']

    #Writing the output to a file 
    df_raw.to_csv(result_file, index=False)

    #Printing the output
    print("Output : ", result_file)

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Error : Invalid number of arguments")
        sys.exit(1)

    #Reading the input arguments
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_file = sys.argv[4]

    #Calling the topsis function
    topsis(input_file, weights, impacts, result_file)