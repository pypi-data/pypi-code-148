def topsis(df,weights,impacts,df1):
    import pandas as pd
    import numpy as np
    import sys

    col= len(df.axes[1])
    row= len(df.axes[0])
    if (col<3):
        print("invalid number of columns")
        sys.exit()
    if(col!=len(impacts)):
        print("Invalid number of impacts")
        sys.exit()
    if(col!=len(weights)):
        print("Invalid number of weights")
        sys.exit()
    #normalize
    sum = [0 for element in range(col)]
    for i in range(row):
        for j in range(col):
            sq=df.iloc[i,j]
            sq=sq**2
            sum[j]+= (sq)
    for i in range(row):
        for j in range(col):
            df.iloc[i,j]/=sum[j]
            df.iloc[i,j]*=weights[j]
    #ideal best and worst
    ibest=df.max()
    iworst=df.min()
    for i in range(col):
        if(impacts[i] =='-'):
            t=ibest[i]
            ibest[i]=iworst[i]
            iworst[i]=t
    #euclidean distance
    eubest = 0
    euworst = 0 
    eubest = [0 for element in range(row)]
    euworst = [0 for element in range(row)]
    for i in range(row):
        for j in range(col):
            a=df.iloc[i,j]-ibest[j]
            eubest[i]+=(a)**2
            euworst[i]+=(df.iloc[i,j]-iworst[j])**2
        eubest[i]=eubest[i]**0.5
        euworst[i]=euworst[i]**0.5
    #performance score
    perf = [0 for element in range(row)] 
    for i in range(row):
        perf[i]=eubest[i]/(eubest[i]+euworst[i])
    df['Performance Score']=perf
    df['Rank'] = (df['Performance Score'].rank(method='max', ascending=False))
    df=df.astype({"Rank":int})
    df.to_csv(sys.argv[4])


if len(sys.argv)!=5:
    print("Invalid number of arguments")
    sys.exit()


filename=sys.argv[1]
try:
    data = pd.read_excel(filename)
except FileNotFoundError:
    print("No such file")
    print("excetption handled")
    sys.exit()
weights=[]
impacts=[]
for item in sys.argv[2].split(","):
    if item.isdigit():
        weights.append(int(item))
    else:
        print("invalid weights")
        sys.exit()
for item in sys.argv[3].split(","):
    if item=='-' or item=='+':
        impacts.append((item))
    else:
        print("invalid impact")
        sys.exit()

df=pd.DataFrame(data)
df =df.iloc[:,1:]
topsis(df,weights,impacts,df)