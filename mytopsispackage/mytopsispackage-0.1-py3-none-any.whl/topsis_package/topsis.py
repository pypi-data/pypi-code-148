def topsis(dummy,df,weights,impacts,output_name):
    import sys
    import pandas as pd 
    import numpy as np
    import os
    import copy
    df1=copy.deepcopy(df)
    df =df.iloc[:,1:]

    colsize=len(df.axes[1])
    rowsize=len(df.axes[0])
    if colsize<3:
        print("invalid number of columns")
        sys.exit()

    if(colsize!=len(impacts)):
        print("Invalid number of impacts",len(impacts),colsize)
        sys.exit()
    if(colsize!=len(weights)):
        print("Invalid number of weights")
        sys.exit()
    for i in range(colsize):
        temp=0
        for j in range(rowsize):
            temp=temp+df.iloc[j,i]
        for j in range(rowsize):
            df.iloc[j,i]=df.iloc[j,i]*weights[i-1]/temp
    best=df.max()
    worst=df.min()
    #print(df)
    for i in impacts:
        if i=='-':
            best[i],worst[i]=worst[i],best[i]
    
    score = [] 
    p = [] 
    n = [] 
 


    for i in range(len(df)):
        temp_p, temp_n = 0, 0
        for j in range(1, colsize):
            temp_p = temp_p + (best[j-1] - df.iloc[i, j])**2
            temp_n = temp_n + (worst[j-1] - df.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
        n.append(temp_n)
        p.append(temp_p)
        
    
    df1['score']=score
    df1['Rank'] = (df1['score'].rank(method='max', ascending=False))
    df1 = df1.astype({"Rank": int})
    print(df1)
    df1.to_csv(output_name)
