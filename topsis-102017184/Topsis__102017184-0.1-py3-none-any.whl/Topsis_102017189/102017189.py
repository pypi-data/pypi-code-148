#102017189
#Vishalakshi
#CSE 8

import sys
import pandas as pd
import numpy as np

#checking Parameters and showing error messages
try:
    t=open(sys.argv[1])
except:
        raise Exception("You have added wrong file or file path")
f=pd.read_csv(sys.argv[1])
f2=pd.read_csv(sys.argv[1])
if(len(f.columns)<2):
    raise Exception('more than 2 columns should exist')
f1=f.dtypes
print(f1)
if(list(f1).count('float64')==f.shape[1]):
    raise Exception('numeric values must exist')
w=[]
for i in sys.argv[2].replace('"','').split(','):
    w.append(int(i))
if(len(f.columns[1:])!=len(w)):
    raise Exception('the length of weight should be equal to number of columns')
impt=[]
for i in sys.argv[3].replace('"','').split(','):
    impt.append(i)
if(len(f.columns[1:])!=len(w)):
    raise Exception('the length of impact should be same with number of columns')
print(impt)
for i in impt:
    if(i!='+' and i!='-'):
        raise Exception('the impact should consist of + and -')
print(w)


pd.set_option('mode.chained_assignment', None)
y=0


for i in f.columns[1:]:
    np_1 = np.square(f[i])
    sum_1 = sum(np_1)
    for j in f.index:
        f.loc[j, i] = f.loc[j, i] / sum_1 ** 0.5
for i in f.columns[1:]:
    for j in f.index:
        f.loc[j,i]=f.loc[j,i]*w[y]
    y+=1
val_p=[]
val_m=[]
y=0


for i in f.columns[1:]:
    if(impt[y]=='+'):
        val_p.append(f[i].max())
        val_m.append(f[i].min())
    else:
        val_m.append(f[i].max())
        val_p.append(f[i].min())
    y+=1
t_p=[]
t_m=[]
y=0


for i in f.index:
    temp_1=0
    temp_2=0
    y=0
    for j in f.columns[1:]:
        temp_1+=(f[j][i]-val_p[y])**2
        temp_2+=(f[j][i]-val_m[y])**2
        y+=1
    t_p.append(temp_1**0.5)
    t_m.append(temp_2**0.5)

#Calculating Performance    
performance=[]

for i in range(len(f.index)):
    performance.append(t_m[i]/(t_m[i]+t_p[i]))
print(performance)

#Result - Printing rank 

f2[' Topsis score ']=performance
list_f=list(sorted(performance,reverse=True).index(x)+1 for x in performance)
f2[' Rank ']=list_f

#getting result as csv
f2.to_csv('result.csv', index=False)