desc = '''Script implementing TOPSIS.

Usage: python Topsis.py <inputDataFile> <weights> <impacts> <outputFile>

The script will rank the objects on the basis of the
<weights> and <impacts> of their attributes.

All the attributes should be either float type
or string type.

For attributes which are string type, the following
table is used.

    low                     1
    below average           2
    average                 3
    good                    4
    excellent               5

The ranked table will be saved in the <outputFile>.

'''
import os
import sys
import pandas as pd
import numpy as np
import math

def topsis():
    try:
        input_file = sys.argv[1]
        
        n1 = len(sys.argv[2])
        weights = sys.argv[2]
        weights=weights.split(',')
        
        n2 = len(sys.argv[3])
        impacts = sys.argv[3][0:n2]
        impacts = impacts.split(',')
        
        output_file = sys.argv[4]
    except:
        print("Arguments missing.")
        print(desc)
        exit(-1)

    input_file_path = os.path.join(os.getcwd(), input_file)
    isFile = os.path.isfile(input_file_path)
    if not isFile:
        print(input_file)
        print(input_file_path)
        raise Exception("File does not exist")
        exit(-1)

    inp_df = pd.read_csv(input_file)
    op_df = pd.read_csv(input_file)
    cols=inp_df.shape[1]
    rows=inp_df.shape[0]
    ###########################################################
    # checking the number of elements in the arguments

    if len(weights)!=cols-1:
        raise Exception("Number of weights are not sufficient")

    if len(impacts)!=cols-1:
        raise Exception("Number of impacts are not sufficient")

    for i in range(len(weights)):
        weights[i] = float(weights[i])

    ############################################################
    # handling string columns
        
    scale_def = {"low" : 1 , "below average":2, "average":3, "good":4, "excellent":5}
    string_col = []
    for i in range(cols):
        if i == 0:
            continue
        
        if type(inp_df.iloc[1,i]) == str:
            string_col.append(i)
            
    for i in string_col:
        for j in range(rows):
            inp_df.iloc[j,i] = scale_def[inp_df.iloc[j,i]]
        
            
    ############################################################
    # make a normalized matrix, (element/perf_score)*weight

    perf_score = []
    for i in range(cols):
        if i==0:
            continue
        
        perf = math.sqrt(sum(inp_df.iloc[:,i]**2))
        perf_score.append(perf)
        inp_df.iloc[:,i] = inp_df.iloc[:, i]/perf
        inp_df.iloc[:,i] = inp_df.iloc[:,i]*weights[i-1]
        
    ###########################################################
    # calculate best and worst score

    best_score = []
    worst_score = []

    for i in range(cols):
        if i==0:
            continue
        
        if impacts[i-1] == '+':
            x = inp_df.iloc[:,i].max()
            best_score.append(x)
            y = inp_df.iloc[:,i].min()
            worst_score.append(y)
            
        else:
            x = inp_df.iloc[:,i].min()
            best_score.append(x)
            y = inp_df.iloc[:,i].max()
            worst_score.append(y)
            
    ##########################################################
    # calculating new column score

    pos_score = []
    neg_score = []
    pos = 0
    neg = 0
    for i in range(rows):
        for j in range(cols):
            if j==0:
                continue
            
            pos = pos + (inp_df.iloc[i,j] - best_score[j-1])**2
            neg = neg + (inp_df.iloc[i,j] - worst_score[j-1])**2
        
        # these store the values of every elemnts pos and neg score 
        #           -> they are two new seperate columns
        pos_score.append(math.sqrt(pos))
        neg_score.append(math.sqrt(neg))
        pos=0
        neg = 0

    #####################################################################
    # calculate the final performance score

    fin_perf_score = []
    for i in range(len(pos_score)):
        cal = neg_score[i]/(pos_score[i] + neg_score[i])
        fin_perf_score.append(cal)
        
    inp_df['Performance'] = fin_perf_score
    op_df['Topsis_Score'] = fin_perf_score

    #####################################################################
    # ranking the models
    inp_df["Rank"] = inp_df["Performance"].rank(ascending=False)
    op_df["Rank"] = op_df["Topsis_Score"].rank(ascending=False)

    #####################################################################
    # writing to the file

    op_df.to_csv(output_file, index = False)


if __name__ == "__main__":
    topsis()