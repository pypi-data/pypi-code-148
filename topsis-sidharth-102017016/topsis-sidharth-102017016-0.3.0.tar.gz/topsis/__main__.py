import pandas as pd
import numpy as np
import sys
import os

def topsis(df, weights, criteria,resultFilePath):
    df2 = df.iloc[:, 1:]
    
    df2 = df2.apply(lambda x: x / np.sqrt(np.sum(np.square(x))), axis=0)
    
    df2 = df2 * weights
    
    rows, cols = df2.shape
    df2_ideal_best = []
    df2_ideal_worst = []

    for i in range(cols):
        if criteria[i] == '-':
            df2_ideal_best.append(df2.iloc[:, i].min())
            df2_ideal_worst.append(df2.iloc[:, i].max())
        else:
            df2_ideal_best.append(df2.iloc[:, i].max())
            df2_ideal_worst.append(df2.iloc[:, i].min())
    df2_s_best = []
    df2_s_worst = []
    for i in range(rows):
        df2_s_best.append(np.sqrt(np.sum(np.square(df2.iloc[i, :] - df2_ideal_best))))
        df2_s_worst.append(np.sqrt(np.sum(np.square(df2.iloc[i, :] - df2_ideal_worst))))

    topsis_score = [x/(x+y) for x, y in zip(df2_s_worst, df2_s_best)]

    sorted_score = sorted(topsis_score, reverse=True)

    topsis_rank = [sorted_score.index(x)+1 for x in topsis_score]

    df = df.assign(topsis_score=topsis_score, topsis_rank=topsis_rank)
    df = df.rename(columns={'topsis_score': 'Topsis Score', 'topsis_rank': 'Rank'})
    df.to_csv(resultFilePath, index=False)

def main():
    numArgs = len(sys.argv)
    if numArgs != 5:
        print("Invalid number of arguments")
        exit(0)

    inputFilePath = sys.argv[1]
    weights = sys.argv[2]
    criteria = sys.argv[3]

    resultFilePath = sys.argv[4]

    if os.path.isfile(inputFilePath) == False:
        print("Invalid input file path")
        exit(0)

    df = pd.read_csv(inputFilePath)
    rows,cols = df.shape
    if cols<3:
        print("File should have atleast 3 columns")
        exit(0)

    if weights.__contains__(',') == False:
        print("Weights should be separated by comma")
        exit(0)

    if criteria.__contains__(',') == False:
        print("Weights should be separated by comma")
        exit(0)

    weights = weights.split(',')
    criteria = criteria.split(',')

    weights = [float(x) for x in weights]
    if(len(weights) != cols-1):
        print("Number of weights should be " + str(cols-1))
        exit(0)

    if(len(criteria) != cols-1):
        print("Number of criteria should be " + str(cols-1))
        exit(0)

    for c in criteria:
        if  c not in ['+', '-']:
            print("Criteria should be either + or -")
            exit(0)

    topsis(df, weights, criteria,resultFilePath)



if __name__ == '__main__':
    main()