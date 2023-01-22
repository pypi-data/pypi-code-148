import numpy as np
import pandas as pd
import math
import sys
import logging

def topsis_score(inputFileName,weights,impact,outputFileName):
    
    #if input file does not exist
    try:
        df=pd.read_csv(inputFileName)
        original_df = df.copy(deep=True)
    except FileNotFoundError:
        print("Error: Input file does not exist")
        raise
    #if there are less than 3 columns
    if len(df.columns)<3:
        print("Error: data must contain three or more columns")
        quit()
    #if there is non numeric value in any column
    abc=[]
    for i in df.columns:
        abc.append(i)
    abc.pop(0)
    for i in abc:
        if df[i].dtype!=np.int64 and df[i].dtype!=np.float64:
            sys.stdout.write("Atleast one column with non-numeric data type.")
            sys.exit(0)
    
    rows = len(df)
    columns = len(df.columns)
    #weights=np.array(weights.split(','))
    #impact=np.array(impact.split(','))
    print(columns)
    print(len(weights))
    #no of weights,no of impacts and columns should be same
    if columns-1!=len(weights) and columns-1!=len(impact):
        logging.error("Number of weights or impacts are not same as number of columns")
        return

    #if weights are not seperated by ,
    if ',' not in weights:
         print("Error: Weights should be separated by ','")
         return
    weights=weights.split(',')

    #if impact are not seperated by ,
    impact=impact
    if ',' not in impact:
         print("Error: Impacts should be separated by ','")
         return
    impact = impact.split(',')

   #Impact must contain + or -
    for i in impact:
        if i!='+' and i!='-':
            print("Error: Impact must contain '+' or '-'")
            return
        
    for i in range(1,columns):
        temp = 0
        for j in range(rows):
            temp = temp + df.iloc[j,i]**2
        temp=temp**0.5
        for j in range(rows):
            df.iloc[j,i]=df.iloc[j,i]/temp
            df.iloc[j,i]=df.iloc[j,i]*int(weights[i-1])


    df_new = df.drop(df.columns[0],axis=1)
    ideal_best_array = df_new.max().values
    ideal_worst_array = df_new.min().values

    best_worst_array=[]
    for i in range(len(ideal_best_array)):
        if impact[i]=='+':
            best_worst_array.append([ideal_best_array[i],ideal_worst_array[i]])
        else:
            best_worst_array.append([ideal_worst_array[i],ideal_best_array[i]])
            
    best_worst_array=np.array(best_worst_array)
    best_worst_array


    distance_pos=[]
    distance_neg=[]
    score = []

    for i in range(rows):
        temp_pos=0
        temp_neg=0
        
        for j in range(len(df_new.columns)):
            
            temp_pos=temp_pos + (best_worst_array[j,0]-df_new.iloc[i,j])**2
            temp_neg = temp_neg + (best_worst_array[j,1]-df_new.iloc[i,j])**2
        temp_pos=temp_pos**0.5
        temp_neg=temp_neg**0.5
        distance_pos.append(temp_pos)
        distance_neg.append(temp_neg)
        score.append(temp_neg/(temp_neg+temp_pos))
        
    df['Topsis score']=score
    df['Rank']=df['Topsis score'].rank(ascending=False)
    df=df.astype({'Rank':int})
    original_df['Topsis score']=df['Topsis score']
    original_df['Rank']=df['Rank']
    original_df
    original_df.to_csv(outputFileName,index=False)
    print("Output file generated")
# if __name__=="__main__":
# 	topsis_score()	