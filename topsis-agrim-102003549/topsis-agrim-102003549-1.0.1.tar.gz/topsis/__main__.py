
import pandas as pd
import numpy as np
import sys
import os
from pandas.api.types import is_numeric_dtype
from detect_delimiter import detect

if(len(sys.argv)!=5):
    print("Incorrect Number of arguments")
    exit(0)
# try:
dataloc,weights,impact,finaldata=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
# except 

# if(not(os.path.isdir(dataloc))):
#     print("File Doesn't Exist")
# print(len(sys.argv))
# print(dataloc)

if(not (dataloc.endswith(".csv") )):
    print("Input File should be in csv format")
    exit(0)
if(not (finaldata.endswith(".csv") )):
    print("Output File should be in csv format")
    exit(0)
if(detect(impact)!=","):
    print("Impacts should be seperated by commas(,)")
    exit(0)
impact = impact.split(",")
if(detect(weights)!=","):
    print("Weights should be seperated by commas(,)")
    exit(0)
weights = list(map(int,weights.split(",")))

for i in set(impact):
    # print(i)
    if(i not in {'+','-'}):
        print("Impacts should only contain '+' or '-'")
        exit(0)

try:
    data = pd.read_csv(dataloc)
except OSError:
    print("File Doesn't Exists")
    exit(0)
# data
if(data.dtypes[0]!=object):
    print("First Column should be object/variable name")
    exit(0)
if(data.shape[1]<3):
    print("Input file must contain 3 or more columns ")
    exit(0)
for i in range(1,data.shape[1]):
    if(not(is_numeric_dtype(data.dtypes[i]))):
        print("Datatype of all columns except first should be numeric")
        exit(0)
if(len(weights)!= len(impact) or len(weights)!= data.shape[1]-1):
    print("Incorrect number of weights/impacts")
    exit(0)

# from sklearn.preprocessing import OrdinalEncoder
# data.shape
# label=data["Fund Name"]
# label
# label=data.pop("Fund Name")
# label,features=data.iloc[:,[0]],data.iloc[:,1:]
# print(label)
# print(features)


rsq = []
# print(data.iloc[2][3])
for i in range(1,data.shape[1]):
    sum=0
    for j in range(data.shape[0]):
        sum+=data.iloc[j][i]**2
    sum = sum **(0.5)
    rsq.append(sum)
# rsq
# data




scaled_data = data
# print(type(data))
# print(type(scaled_data))
# print(scaled_data.info())
# scaled_data.shape
for i in range(1,scaled_data.shape[1]):
    
    for j in range(scaled_data.shape[0]):
        # print(i,j)
        scaled_data.iat[j,i]=data.iloc[j][i]/rsq[i-1]
        # print(rsq[i-1])
print(scaled_data)


import copy
# weights=[1,1,1,1,1]
w_scaled_data=copy.deepcopy(scaled_data)
for i in range(w_scaled_data.shape[0]):
    
    for j in range(1,w_scaled_data.shape[1]):
        w_scaled_data.iat[i,j]=weights[j-1]*scaled_data.iloc[i][j]
# w_scaled_data


IB=(w_scaled_data.max().values)[1:]
IW=(w_scaled_data.min().values)[1:]
# print(IB,IW)



# impact = ["+","-","+","+","+"]
for i in range(len(impact)):
    if impact[i]=="-":
        IB[i],IW[i]=IW[i],IB[i]
# print(IB,IW)


dp=[]
dn=[]
for i in range(w_scaled_data.shape[0]):
    tdp=0 
    tdn=0
    for j in range(1,w_scaled_data.shape[1]):
        tdp+=(w_scaled_data.iloc[i][j]-IB[j-1])**2
        tdn+=(w_scaled_data.iloc[i][j]-IW[j-1])**2
    dp.append(tdp**0.5)
    dn.append(tdn**0.5)

# print(dp,dn)


# w_scaled_data['distance positive']=dp
# w_scaled_data['distance negative']=dn


scores=[]
for i in range (len(dp)):
    scores.append(dn[i]/(dp[i]+dn[i]))
print(scores)
w_scaled_data['topsis score']=scores


w_scaled_data['rank']=w_scaled_data['topsis score'].rank(method='max',ascending=False)

w_scaled_data = w_scaled_data.astype({"rank": int})
print(w_scaled_data)

w_scaled_data.to_csv(finaldata)



