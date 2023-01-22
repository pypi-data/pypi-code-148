#Name: Ishita Kaundal
#Roll No.: 102017184
#Subgroup: CSE-8

from tabulate import tabulate
from os import path
import pandas as pd
import math as m
import sys

def topsis(filename, weight, impact, Result_file):
    # LOADING DATASET
    dataset = pd.read_csv('102017184-data.csv')

    # DROPpiNG EMPTY CELLS IF ANY
    dataset.dropna(inplace = True)

    # ONLY TAKING NUMERICAL VALUES
    d = dataset.iloc[0:,1:].values

    # CONVERTING INTO mat
    mat = pd.DataFrame(d)

    # CALCULATING SUM OF SQUARES
    sum_of_squares = []
    for col in range(0, len(mat.columns)):
        X = mat.iloc[0:,[col]].values
        sum = 0
        for value in X:
            sum = sum + m.pow(value, 2)
        sum_of_squares.append(m.sqrt(sum))
    

    # DIVIDING ALL THE VALUES BY SUM OF SQUARES
    j = 0
    while(j < len(mat.columns)):
        for i in range(0, len(mat)):
            mat[j][i] = mat[j][i]/sum_of_squares[j] 
        j = j+1

    # MULTIPLYING BY weight
    k = 0
    while(k < len(mat.columns)):
        for i in range(0, len(mat)):
            mat[k][i] = mat[k][i]*weight[k] 
        k = k+1

    # CALCULATING IDEAL BEST AND IDEAL WORST
    bestValue = []
    worstValue = []

    for col in range(0, len(mat.columns)):
        Y = mat.iloc[0:,[col]].values
        
        if impact[col] == "+" :
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(maxValue[0])
            worstValue.append(minValue[0])

        if impact[col] == "-" :
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(minValue[0])
            worstValue.append(maxValue[0])

    # CALCULATING Si+ & Si-
    si_plus = []
    si_minus = []

    for row in range(0, len(mat)):
        temp = 0
        temp2 = 0
        wholeRow = mat.iloc[row, 0:].values
        for value in range(0, len(wholeRow)):
            temp = temp + (m.pow(wholeRow[value] - bestValue[value], 2))
            temp2 = temp2 + (m.pow(wholeRow[value] - worstValue[value], 2))
        si_plus.append(m.sqrt(temp))
        si_minus.append(m.sqrt(temp2))

    # CALCULATING PERFORMANCE SCORE pi
    pi = []

    for row in range(0, len(mat)):
        pi.append(si_minus[row]/(si_plus[row] + si_minus[row]))

    # CALCULATING RANK
    Rank = []
    sortedpi = sorted(pi, reverse = True)

    for row in range(0, len(mat)):
        for i in range(0, len(sortedpi)):
            if pi[row] == sortedpi[i]:
                Rank.append(i+1)

    # INSERTING THE NEWLY CALCULATED COLUMNS INTO THE MATRIX
    col1 = dataset.iloc[:,[0]].values
    mat.insert(0, dataset.columns[0], col1)
    mat['Topsis Score'] = pi
    mat['Rank'] = Rank

    # RENAMING ALL THE COLUMNS
    newColNames = []
    for name in dataset.columns:
        newColNames.append(name)
    newColNames.append('Topsis Score')
    newColNames.append('Rank')
    mat.columns = newColNames

    # SAVING THE mat INTO A CSV FILE
    mat.to_csv('102017184-result.csv')

    # PRINTING TO THE CONSOLE USING TABULATE PACKAGE
    print(tabulate(mat, headers = mat.columns))

def checkRequirements() :
    if len(sys.argv) == 5 :
        # filename
        filename = sys.argv[1].lower()
        # weight
        weight = sys.argv[2].split(",")
        for i in range(0, len(weight)):
            weight[i] = int(weight[i])
        # impact
        impact = sys.argv[3].split(",")
        # Result_file
        Result_file = sys.argv[-1].lower()
        if ".csv" not in Result_file:
            print("Result file must contain '.csv'")
            return
        if path.exists(filename) :
            if len(weight) == len(impact) :
                topsis(filename, weight, impact, Result_file)
            else :
                print("Number of weights must be equal to the number of impacts!!")
                return
        else :
            print("Input file does not exist!!")
            return
    else :
        print("Required number of arguments are not provided!!")
        return

    for i in impact:
      if(i!='+' and i!='-'):
        print("The impacts must be either +ve or -ve!!")

    f=pd.read_csv(sys.argv[1])
    if(len(f.columns)<2):
      print("There must be more than 2 columns!!")

checkRequirements()