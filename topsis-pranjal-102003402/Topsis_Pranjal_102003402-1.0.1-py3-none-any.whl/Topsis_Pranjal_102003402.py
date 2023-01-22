#ASSIGNMENT1- SUBMISSION BY PRANJAL ARORA, 102003402, 3COE-16

#QUESTION 2 - for topsis package

import sys
import pandas as pd
import numpy as np
import logging

def topsis():
    if len(sys.argv)!=5:
        logging.warning('ERROR! Wrongly inputting the arguments from commmand line')
        # print("ERROR! Wrongly inputting the arguments from commmand line")
        exit()
    try:
        with open(sys.argv[1], 'r') as data1:
            df=pd.read_csv(data1)
    except FileNotFoundError:
        logging.warning('ERROR! Could not find the csv file.')
        # print("ERROR! Could not find the csv file.")
        exit()

    dataframe=pd.DataFrame(data=df)

    #inputting weights, impacts and getting number of columns
    weight = list(sys.argv[2].split(","))
    impactsign = list(sys.argv[3].split(","))
    
    #count number of columns in the dataframe
    no_of_col = len(dataframe.columns)

    #making key-value pairs for special characters encountered:-

    #with + and - signs
    spchar = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '+': True, '*': True,'-': True, '=': True}
    #without + and - signs
    specialchar = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '*': True, '=': True}


    #functions for validating characters and strings in the command line
    def spchar_validator(list1, spchar_keyval):
        for element in list1:
            for char in element:
                if char in spchar_keyval:
                    return False

    def strfind(list2, spchar_keyval):
        for string in list2:
            list1 = string.split(",")
            if spchar_validator(list1, spchar_keyval) == False:
                logging.warning('ERROR! CSV format not found')
                # print("ERROR! not CSV ")
                exit()

    strfind(sys.argv[2], spchar)
    strfind(sys.argv[3], specialchar)

    #checks on dimensions of datset
    if no_of_col<=2:
        logging.warning('COLUMNS MUST BE GREATER THAN 2')
        # print("COLUMNS MUST BE GREATER THAN 2")
        exit()

    if len(impactsign) != (no_of_col-1):
        logging.warning('INPUT EQUAL NUMBER OF IMPACT SIGNS AND COLUMNS')
        # print("INPUT EQUAL NUMBER OF IMPACT SIGNS AND COLUMNS")
        exit()

    if len(weight) != (no_of_col-1):
        logging.warning('INPUT EQUAL NUMBER OF WEIGHTS AND COLUMNS')
        # print("INPUT EQUAL NUMBER OF WEIGHTS AND COLUMNS")
        exit()

    #check impact signs
    lis = {'-','+'}
    if set(impactsign) != lis:
        logging.warning('MAKE SURE IMPACT CAN BE '+' OR '-' ONLY')
        # print("MAKE SURE IMPACT CAN BE '+' OR '-' ONLY")
        exit()


    #convert columns to numeric
    for index,row in dataframe.iterrows():
        try:
            float(row['P1'])
            float(row['P2'])
            float(row['P3'])
            float(row['P4'])
            float(row['P5'])
        except:
            dataframe.drop(index,inplace=True)
    dataframe["P1"] = pd.to_numeric(dataframe["P1"], downcast="float")
    dataframe["P2"] = pd.to_numeric(dataframe["P2"], downcast="float")
    dataframe["P3"] = pd.to_numeric(dataframe["P3"], downcast="float")
    dataframe["P4"] = pd.to_numeric(dataframe["P4"], downcast="float")
    dataframe["P5"] = pd.to_numeric(dataframe["P5"], downcast="float")
    df1 = dataframe.copy(deep=True)



    #following the topsis algorithm to find ideal best and ideal worst, using topsis score and rank

    #first making normalizing function
    def normalizing_column(df, no_of_column, weights):
        for i in range(1, no_of_column):
            temp = 0
            for j in range(len(df)):
                temp = temp + df.iloc[j, i]**2
            temp = temp**0.5
            for j in range(len(df)):
                df.iat[j, i] = (float(df.iloc[j, i])) / float(temp)*float(weights[i-2])

    #making calculation function using impact signs 
    def calculatevalues(df, no_of_col, weights):
        p1 = (df.max().values)[1:]
        n1 = (df.min().values)[1:]
        for i in range(1, no_of_col):
            if impactsign[i-2] == '-':
                p1[i-1], n1[i-1] = n1[i-1], p1[i-1]
        return p1, n1

    normalizing_column(dataframe,no_of_col,weight)
    p1, n1 = calculatevalues(dataframe, no_of_col, impactsign)
    score = []
    pdist = []  #positive distance
    ndist = []  #negative distance

    #traverse the dataframe fro ideal best and ideal worst
    for i in range(len(dataframe)):
        ptemp, ntemp = 0, 0
        for j in range(1, no_of_col):
            ptemp = ptemp + (p1[j-1] - dataframe.iloc[i, j])**2
            ntemp = ntemp + (n1[j-1] - dataframe.iloc[i, j])**2
        ptemp, ntemp = ptemp*0.5, ntemp*0.5
        score.append(ntemp/(ptemp + ntemp))
        ndist.append(ntemp)
        pdist.append(ptemp)

    ##display topsis score and rank
    df1['Topsis Score'] = score
    df1['Rank'] = (df1['Topsis Score'].rank(method='max', ascending=False))
    df1 = df1.astype({"Rank": int})
    df1.to_csv(sys.argv[4],index=False)
