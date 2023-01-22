import pandas as pd
import numpy as np
import sys
import os

def readAndValidateArguments():

    #check the number of arguments
    numberOfArguments = len(sys.argv)
    if numberOfArguments != 5:
        print("Invalid number of arguments")
        exit(0)

    #read the arguments
    inputFilePath = sys.argv[1]
    weights = sys.argv[2]
    criteria = sys.argv[3]
    resultFilePath = sys.argv[4]
    
    #validate the arguments

    #check if input file exists
    if os.path.isfile(inputFilePath) == False:
        print("Input file does not exist")
        exit(0)
    df = pd.read_csv(inputFilePath)
    rows, cols = df.shape

    #check if weights are valid
    if weights.__contains__(',') == False:
        print("Weights should be separated by comma")
        exit(0)
    weights = weights.split(',')
    weights = [float(x) for x in weights]
    if(len(weights) != cols-1):
        print("Number of weights should be " + str(cols-1))
        exit(0)

    #check if impacts are valid
    if criteria.__contains__(',') == False:
        print("Impact should be separated by comma")
        exit(0)
    criteria = criteria.split(',')
    if(len(criteria) != cols-1):
        print("Number of impact should be " + str(cols-1))
        exit(0)
    for c in criteria:
        if  c not in ['+', '-']:
            print("Impact should be either + or -")
            exit(0)

    #check if result file is valid
    if resultFilePath.__contains__('.csv') == False:
        print("Result file should be csv")
        exit(0)
    return inputFilePath, weights, criteria, resultFilePath


def calculate_topsis_rank(dataframe, weight_vector, criteria_vector, output_path):
    # Normalize the dataframe columns
    normalized_data = dataframe.iloc[:, 1:].div(dataframe.iloc[:, 1:].pow(2).sum(axis=0).pow(0.5), axis=1)
    
    # Apply weight vector to the normalized data
    weighted_data = normalized_data.mul(weight_vector, axis=1)
    
    # Determine the ideal best and worst solutions
    ideal_best = []
    ideal_worst = []
    for i in range(weighted_data.shape[1]):
        if criteria_vector[i] == '-':
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())
        else:
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
    
    # Calculate the separation measure for each solution from the ideal best and worst solutions
    s_best = []
    s_worst = []
    for i in range(weighted_data.shape[0]):
        s_best.append(((weighted_data.iloc[i, :] - ideal_best) ** 2).sum() ** 0.5)
        s_worst.append(((weighted_data.iloc[i, :] - ideal_worst) ** 2).sum() ** 0.5)
    
    # Calculate the TOPSIS score and rank for each solution
    topsis_score = [x / (x + y) for x, y in zip(s_worst, s_best)]
    sorted_scores = sorted(topsis_score, reverse=True)
    topsis_rank = [sorted_scores.index(x) + 1 for x in topsis_score]
    
    # Add the TOPSIS score and rank columns to the dataframe
    dataframe = dataframe.assign(topsis_score=topsis_score, topsis_rank=topsis_rank)
    dataframe = dataframe.rename(columns={'topsis_score': 'TOPSIS Score', 'topsis_rank': 'Rank'})
    
    # Output the dataframe to a CSV file
    dataframe.to_csv(output_path, index=False)

def main():
    inputFilePath, weightVector, criteriaVector, resultFilePath = readAndValidateArguments()
    dataframe = pd.read_csv(inputFilePath)
    calculate_topsis_rank(dataframe, weightVector, criteriaVector, resultFilePath)


if __name__ == "__main__":
    main()
