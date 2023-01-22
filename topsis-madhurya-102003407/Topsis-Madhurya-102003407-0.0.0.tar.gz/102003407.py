import pandas as pd
import numpy as np
import sys
import os

#sys.argv() is an array for command line arguments in Python
#we are checking if all the 5 arguments are entered or not
def topsis(filename,w,imp,file2):
  if len(sys.argv)!=5:
      raise Exception('Wrong Format, Write: python <program.py> <InputDataFile.csv> <Weights> <Impacts> <output.csv>')
      exit()

  # open(sys.argv[1], 'r')  open a file, read all the lines out of it, handling one line at a time, 'r' means reading.
  try:
      with open(sys.argv[1], 'r') as filee:
              df=pd.read_csv(filee)
              
  except FileNotFoundError:
          print("File not found")
          exit()

  punctuation_dictionary = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '+': True, '*': True,'-': True, '=': True}
  punctuation_dictionary2 = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '*': True, '=': True}

  #to check if the input is valid
  def char_check(new_list, punct_dict):
          for item in new_list:
              for char in item:
                  if char in punct_dict:
                      return False
  #to check if the input is comma seperated
  def string_check(comma_check_list, punct_dict):
          for string in comma_check_list:
              new_list = string.split(",")
              if char_check(new_list, punct_dict) == False:
                  print("Invalid input or Values not comma separated")
                  exit()

  string_check(sys.argv[2], punctuation_dictionary)
  string_check(sys.argv[3], punctuation_dictionary2)

  nCol=len(df.columns)
  #creating a list of weights and impacts
  weights1 = list(sys.argv[2].split(","))
  impacts = list(sys.argv[3].split(","))

  weights = [eval(i) for i in weights1]

  #making sure the input is entered properly
  if len(impacts) != (nCol-1) or len(weights) != (nCol-1):
              raise Exception('Lengths of weights and impacts must be same as that of columns!')

  for i in range(len(impacts)):
      if(impacts[i]!="+" and impacts[i]!="-"):
        print("Impacts should be either '+' or '-'.")
        exit()


  col_names = list(df.columns[1:])
  for i in col_names:
    for j in df[i]:
      if not isinstance(j, int) and not isinstance(j, float):
        raise Exception('Value not numeric')

  #iloc helps us to select a specific row or column from the data set.
  #first we are calculating root of sum of squares(temp) and then we are normalizing by 
  #dividing temp with each element and then multiplying the weights to the normalized values
  for i in range(1,nCol):
    temp=0
    for j in range(len(df)):
      temp=temp+df.iloc[j,i]**2
    temp=temp**0.5
    for j in range(len(df)):
      df.iat[j, i] = (df.iloc[j, i] / temp)*weights[i-1]

  #finding ideal best and worst
  ideal_best=(df.max().values)[1:]
  ideal_worst=(df.min().values)[1:]

  for i in range(1,nCol):
    if(impacts[i-1]=='-'):
      ideal_best[i-1],ideal_worst[i-1]=ideal_worst[i-1],ideal_best[i-1]

  #finding score with the help of euclidean distance from best and worst 
  score=[]
  for i in range(len(df)):
    temp_p,temp_n=0,0
    for j in range(1,nCol):
      temp_p=temp_p + (ideal_best[j-1]-df.iloc[i,j])**2
      temp_n=temp_n + (ideal_worst[j-1]-df.iloc[i,j])**2
    
    temp_p=temp_p**0.5
    temp_n=temp_n**0.5
    score.append(temp_n/(temp_p + temp_n))

  df['Topsis Score']=score

  df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
  df = df.astype({"Rank": int})
  print(df)

  df.to_csv(sys.argv[4],index=False)