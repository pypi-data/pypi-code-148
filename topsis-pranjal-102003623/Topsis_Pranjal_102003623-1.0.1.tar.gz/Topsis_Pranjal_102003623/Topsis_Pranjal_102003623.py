from tabulate import tabulate
from os import path
import pandas as pd
import math as m
import sys
def topsis(filename, weights, impacts, resultFileName):
    df = pd.read_csv(filename)
    df.dropna(inplace = True)
    dp = df.iloc[0:,1:].values
    matrix = pd.DataFrame(dp)
    sumOfSquares = []
    for col in range(0, len(matrix.columns)):
        X = matrix.iloc[0:,[col]].values
        sum = 0
        for value in X:
            sum = sum + m.pow(value, 2)
        sumOfSquares.append(m.sqrt(sum)) 
    j = 0
    while(j < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[j][i] = matrix[j][i]/sumOfSquares[j] 
        j = j+1
    k = 0
    while(k < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[k][i] = matrix[k][i]*weights[k] 
        k = k+1
    bv = []
    wv = []
    for col in range(0, len(matrix.columns)):
        Y = matrix.iloc[0:,[col]].values
        if impacts[col] == "+" :
            maxValue = max(Y)
            minValue = min(Y)
            bv.append(maxValue[0])
            wv.append(minValue[0])
        if impacts[col] == "-" :
            maxValue = max(Y)
            minValue = min(Y)
            bv.append(minValue[0])
            wv.append(maxValue[0])
    SiP = []
    SiM = []
    for row in range(0, len(matrix)):
        temp_1 = 0
        temp_2 = 0
        wholeRow = matrix.iloc[row, 0:].values
        for value in range(0, len(wholeRow)):
            temp_1 = temp_1 + (m.pow(wholeRow[value] - bv[value], 2))
            temp_2 = temp_2 + (m.pow(wholeRow[value] - wv[value], 2))
        SiP.append(m.sqrt(temp_1))
        SiM.append(m.sqrt(temp_2))
    Ps = []
    for row in range(0, len(matrix)):
        Ps.append(SiM[row]/(SiP[row] + SiM[row]))
    Rank = []
    sortedPs = sorted(Ps, reverse = True)
    for row in range(0, len(matrix)):
        for i in range(0, len(sortedPs)):
            if Ps[row] == sortedPs[i]:
                Rank.append(i+1)
    col1 = df.iloc[:,[0]].values
    matrix.insert(0, df.columns[0], col1)
    matrix['Topsis Score'] = Ps
    matrix['Rank'] = Rank
    newColNames = []
    for name in df.columns:
        newColNames.append(name)
    newColNames.append('Topsis Score')
    newColNames.append('Rank')
    matrix.columns = newColNames
    matrix.to_csv(resultFileName)
    print(tabulate(matrix, headers = matrix.columns))
def checkInputRequirements() :
    if len(sys.argv) == 5 :
        filename = sys.argv[1].lower()
        weights = sys.argv[2].split(",")
        for i in range(0, len(weights)):
            weights[i] = int(weights[i])
        impacts = sys.argv[3].split(",")
        resultFileName = sys.argv[-1].lower()
        if ".csv" not in resultFileName:
            print("The result filename should include'.csv'")
            return
        if path.exists(filename) :
            if len(weights) == len(impacts) :
                topsis(filename, weights, impacts, resultFileName)
            else :
                print("The number of weights and impacts you are inputting are not equal")
                return
        else :
            print("The dataset you are trying to input does not exist")
            return
    else :
        print("Provide 4 arguments aong with the name of the code file")
        print("You should enter the name of the dataset, the weights, the impacts and the name of the output file")
        return
checkInputRequirements()