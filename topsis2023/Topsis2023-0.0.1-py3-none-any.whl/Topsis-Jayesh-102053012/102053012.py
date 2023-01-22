import pandas as pd
import os
import sys

def start():
    if len(sys.argv)!=5:
        print("Wrong numbers of parameters.")
        exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print("File not found")
        exit(1)
    else:
        dataset,dataset2=pd.read_csv(sys.argv[1]),pd.read_csv(sys.argv[1])
        col_len=len(dataset2.columns.values)
        if col_len<3:
            print("Input file must contain three or more columns.")
            exit(1)
        for num in range(1,col_len):
            pd.to_numeric(dataset.iloc[:, num],errors='coerce')
            dataset.iloc[:, num].fillna((dataset.iloc[:, num].mean()),inplace=True)
        impacts=sys.argv[3].split(',')
        for num in impacts:
            if not (num=='+' or num=='-'):
                print("Wrong inputs in impacts array.")
                exit(1)
        try:
            weights=[int(i) for i in sys.argv[2].split(',')]
        except:
            print("Wrong inputs in weights array.")
            exit(1)
        if col_len-1!=len(weights) or col_len-1!=len(impacts):
            print("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")
            exit(1)
        topsis(dataset2,dataset,col_len,weights,impacts)

def normal(dataset2, col_len, weights):
    for num1 in range(1, col_len):
        temp=0
        for num2 in range(len(dataset2)):
            temp+=dataset2.iloc[num2, num1]**2
            temp=temp**0.5
        for num2 in range(len(dataset2)):
            dataset2.iloc[num2, num1]=(dataset2.iloc[num2,num1]/temp)*weights[num1-1]
    return dataset2

def min_max(dataset2,col_len,impacts):
    pmax=(dataset2.max().values)[1:]
    nmax=(dataset2.min().values)[1:]
    for i in range(1, col_len):
        if impacts[i-1]=='-':
            pmax[i-1],nmax[i-1]=nmax[i-1],pmax[i-1]
    return pmax,nmax

def topsis(dataset2,dataset,col_len,weights,impacts):
    dataset2=normal(dataset2,col_len,weights)
    pmax,nmax=min_max(dataset2,col_len,impacts)
    ans=[]
    for i in range(len(dataset2)):
        temp_p,temp_n=0,0
        for j in range(1, col_len):
            temp_p=temp_p+(pmax[j-1]-dataset2.iloc[i, j])**2
            temp_n=temp_n+(nmax[j-1]-dataset2.iloc[i, j])**2
        temp_p,temp_n=temp_p**0.5,temp_n**0.5
        ans.append(temp_n/(temp_p+temp_n))
    dataset['topsis score']=ans
    dataset['rank']=(dataset['topsis score'].rank(method='max', ascending=False))
    dataset=dataset.astype({'rank': int})
    dataset.to_csv(sys.argv[4], index=False)

if __name__=="__main__":
    start()