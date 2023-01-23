import pandas as pd
import numpy as np
import sys

try:
     with open(sys.argv[1], 'r') as filee:
            df=pd.read_csv(filee)
            
except:
        print("File not found")
        sys.exit(1)

if len(sys.argv)!=5:
    print("Wrong command line input")
    sys.exit(1)

punctuation_dictionary = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '+': True, '*': True,'-': True, '=': True}
punctuation_dictionary2 = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '*': True, '=': True}

def char(new_list, punct_dict):
        for item in new_list:
            for char in item:
                if char in punct_dict:
                    return False

def string(comma_check_list, punct_dict):
        for string in comma_check_list:
            new_list = string.split(",")
            if char(new_list, punct_dict) == False:
                print("Invalid input or Values not comma separated")
                sys.exit(1)

string(sys.argv[2], punctuation_dictionary)
string(sys.argv[3], punctuation_dictionary2)

nCol=len(df.columns)
weights1 = list(sys.argv[2].split(","))
impacts = list(sys.argv[3].split(","))

weights = [eval(i) for i in weights1]

if nCol<3:
        print("No of columns are less than 3.")
        sys.exit(1)

if len(impacts) != (nCol-1):
        print("No of values in impacts should be same as the number of columns.")
        sys.exit(1)

if len(weights) != (nCol-1):
        print("No of values in weights should be same as the number of columns.")
        sys.exit(1)



for i in range(len(impacts)):
    if(impacts[i]!="+" and impacts[i]!="-"):
       print("Impacts should be either '+' or '-'.")
       sys.exit(1)

for index,row in df.iterrows():
        try:
            float(row['P1'])
            float(row['P2'])
            float(row['P3'])
            float(row['P4'])
            float(row['P5'])
        except:
            df.drop(index,inplace=True)
            df["P1"] = pd.to_numeric(df["P1"], downcast="float")
            df["P2"] = pd.to_numeric(df["P2"], downcast="float")
            df["P3"] = pd.to_numeric(df["P3"], downcast="float")
            df["P4"] = pd.to_numeric(df["P4"], downcast="float")
            df["P5"] = pd.to_numeric(df["P5"], downcast="float")
            df = df.copy(deep=True)

for i in range(1,nCol):
  temp=0
  for j in range(len(df)):
    temp=temp+df.iloc[j,i]**2
  temp=temp**0.5
  for j in range(len(df)):
    df.iat[j, i] = (df.iloc[j, i] / temp)*weights[i-1]


ideal_best=(df.max().values)[1:]
ideal_worst=(df.min().values)[1:]

for i in range(1,nCol):
  if(impacts[i-1]=='-'):
    ideal_best[i-1],ideal_worst[i-1]=ideal_worst[i-1],ideal_best[i-1]

score=[]
pos_dist=[]
neg_dist=[]
for i in range(len(df)):
  t_pos,temp_n=0,0
  for j in range(1,nCol):
    t_pos=t_pos + (ideal_best[j-1]-df.iloc[i,j])**2
    temp_n=temp_n + (ideal_worst[j-1]-df.iloc[i,j])**2
  
  t_pos=t_pos**0.5
  temp_n=temp_n**0.5
  score.append(temp_n/(t_pos + temp_n))
  neg_dist.append(temp_n)
  pos_dist.append(t_pos)


df['distance negative']=neg_dist
df['distance positive']=pos_dist
df['Topsis Score']=score

df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
df = df.astype({"Rank": int})
print(df)

df.to_csv(sys.argv[4],index=False)