import pandas as pd
import numpy as np
import sys

def topsis(filename,w,imp,file2):

 try:
     with open(filename, 'r') as filee:
            df=pd.read_csv(filee)
            
 except FileNotFoundError:
        print("File not found")
        exit()

 punctuation_dictionary = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '+': True, '*': True,'-': True, '=': True}
 punctuation_dictionary2 = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '*': True, '=': True}

 def char_check(new_list, punct_dict):
        for item in new_list:
            for char in item:
                if char in punct_dict:
                    return False

 def string_check(comma_check_list, punct_dict):
        for string in comma_check_list:
            new_list = string.split(",")
            if char_check(new_list, punct_dict) == False:
                print("Invalid input or Values not comma separated")
                exit()

 string_check(w, punctuation_dictionary)
 string_check(imp, punctuation_dictionary2)

 nCol=len(df.columns)
 weights1 = list(w.split(","))
 impacts = list(imp.split(","))

 weights = [eval(i) for i in weights1]

 if nCol<3:
        print("No of columns are less than 3.")
        exit()

 if len(impacts) != (nCol-1):
        print("No of values in impacts should be same as the number of columns.")
        exit()

 if len(weights) != (nCol-1):
        print("No of values in weights should be same as the number of columns.")
        exit()



 for i in range(len(impacts)):
    if(impacts[i]!="+" and impacts[i]!="-"):
       print("Impacts should be either '+' or '-'.")
       exit()


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
 distance_positive=[]
 distance_negative=[]
 for i in range(len(df)):
  temp_p,temp_n=0,0
  for j in range(1,nCol):
    temp_p=temp_p + (ideal_best[j-1]-df.iloc[i,j])**2
    temp_n=temp_n + (ideal_worst[j-1]-df.iloc[i,j])**2
  
  temp_p=temp_p**0.5
  temp_n=temp_n**0.5
  score.append(temp_n/(temp_p + temp_n))
  distance_negative.append(temp_n)
  distance_positive.append(temp_p)


 df['distance negative']=distance_negative
 df['distance positive']=distance_positive
 df['Topsis Score']=score

 df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
 df = df.astype({"Rank": int})
 print(df)

 df.to_csv(file2,index=False)