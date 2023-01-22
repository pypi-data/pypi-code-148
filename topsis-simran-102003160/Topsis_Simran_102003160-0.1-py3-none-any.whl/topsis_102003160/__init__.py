def topsis(l,weights,impact):
    import numpy as np
    import pandas as pd
    import sys

    w=[]
    i=[]
    inputFile=l[0]
    w=weights
    i=impact
    try:
        df=pd.read_csv(inputFile)
    except:
        print("File not found")    
    print(df)

    df=df.iloc[:,[1,2,3,4,5]] # excluding the first column
    print(df)
    nCol=len(df.axes[1])

    for i in i:  # to make sure that impacts consist of only + and - values 
            if not (i == '+' or i == '-'):
                print("ERROR : CHECK VALUES OF IMPACT")
                exit(1)

    
                 

    # STEP 2: NORMALISE THE DATA
    norm_data=df/np.sqrt(np.power(df,2).sum(axis=0))
    print("NORM_DATA")
    print(norm_data)

    #STEP 3: MULTIPLY WITH THE WEIGHTS
    norm_w=norm_data*[float(s) for s in w]
    print("NORM_W")
    print(norm_w)

    #STEP 4:IDENTIFY POSITIVE NAD NEGATIVE IDEAL SOLUTIONS
    pos_ideal=norm_w.max()
    neg_ideal=norm_w.min()
    print("POS_IDEAL")
    print(pos_ideal)
    print("NEG_IDEAL")
    print(neg_ideal)

    #STEP 5: SEPARATION MEASUREMENTS
    s_pos=np.sqrt(np.power((norm_w-pos_ideal),2).sum(axis=1))
    s_neg=np.sqrt(np.power((norm_w-neg_ideal),2).sum(axis=1))
    print("S_POS")
    print(s_pos)
    print("S_NEG")
    print(s_neg)

    #STEP 6: CALCULATE PERFORMANCE SCORE
    score=s_neg/(s_neg+s_pos)
    print("SCORE")
    print(score)
    df['SCORE']=score
    print(df)

    df['RATING BASED ON SCORE']=df['SCORE'].rank(ascending=False)
    print("Final dataset")
    print(df)
