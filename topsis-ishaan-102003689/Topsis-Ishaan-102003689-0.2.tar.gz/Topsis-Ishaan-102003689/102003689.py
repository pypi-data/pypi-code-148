import pandas as pd
import sys
import math
import os 
df=pd.read_csv(sys.argv[1])

if df.shape[1]<=3: ## every csv should have more than 3 columns
 print(" No. columns should be greater than 3! ")
 sys.exit(0)

def is_numeric1(t):
        try:
            t=float(t)
            if (isinstance(t, int)==True or isinstance(t, float)==True):
                return True
        except:
            print("Not a numeric value in columns 2nd and above!")
            sys.exit(0)
        return False

for i in range(1,df.shape[1]): ##checking if all the columns fron 2nd have numeric vallues
        for j in range(df.shape[0]):
            if(is_numeric1(df.iloc[j,i]))==False:
                print(df.iloc[j,i])
                print("All the values in 2nd column and further should be numeric")
                sys.exit(0)

w= [int(i) for i in sys.argv[2].split(',')]
im= sys.argv[3].split(',')

impact1=im
totalweight=0.00
weight1=w

for i in range(len(w)):
        totalweight=totalweight+float(w[i])
        if df.shape[1]-1 != len(im) or df.shape[1]-1 != len(w )or len(im)!= len(w):
         print("Either the impacts or weights are not equal to number of columns(starting from 2nd) or the impacts or weights are not separated by commas!")
         sys.exit(0)
for i in im:  ##Impacts must be either +ve or -ve.
        if i not in ["+","-"]:
            print("Impacts should be either + or -!")
            sys.exit(0)



df.drop(df.columns[[0]],axis=1,inplace=True)
df
row=df.shape[0]
col=df.shape[1]
SS=[]
for i in range(0,col):
  sum=0
  for j in range(0,row):
    sum=sum+(df.iloc[j,i]*df.iloc[j,i])
  SS.append(sum)
for i in range(0,col):
  for j in range(0,row):
    df.iloc[j,i]=df.iloc[j,i]/SS[i]
# w=[]
# for i in range(0,col):
#   inp=float(input())
#   w.append(inp)
# w



for i in range(0,col):
  for j in range(0,row):
    df.iloc[j,i]=df.iloc[j,i]*w[i]
df

# word=input()
# im=word.split(",")
# im



max=df.max()
max
min=df.min()
min
vb=[]
for k in range(0,col):
  if(im[k]=='+'):
    vb.append(max[k])
  else:
    vb.append(min[k])

vw=[]
for k in range(0,col):
  if(im[k]=='-'):
    vw.append(max[k])
  else:
    vw.append(min[k])

vw

import numpy as np
df[["Splus","Sminus"]]=np.random.randint(10,size=(row,2))
df

sp=[]
for i in range(0,row):
  val=0
  for j in range(0,col):
    val=val+((df.iloc[i,j]-vb[j])*(df.iloc[i,j]-vb[j]))
    math.sqrt(val)
  sp.append(val)
sp

df['Splus']=sp
df

sm=[]
for i in range(0,row):
  val=0
  for j in range(0,col):
    val=val+((df.iloc[i,j]-vw[j])*(df.iloc[i,j]-vw[j]))
    math.sqrt(val)
  sm.append(val)
sm

df['Sminus']=sm
df

df["Sum"]=(df["Splus"] + df["Sminus"])
df
df["P"]=(df["Sminus"]/(df["Splus"]+df["Sminus"]))
df

df["Rank"]=df["P"].rank(ascending=False)
print(df)
df.to_csv(sys.argv[4])