import pandas as pd
import numpy as np
import logging

def checkParameters(inputFileName,weights,impact):
  try:
      df=pd.read_csv(inputFileName)
      original_df = df.copy(deep=True)
  except FileNotFoundError:
      logging.error("Input file not found")
      return
  if len(df.columns)<3:
      logging.error("Input file must contain 3 or more columns")
      return
  for i in range(1,len(df.columns)):
    try:
        df.iloc[:,i]=pd.to_numeric(df.iloc[:,i])
    except ValueError:
        logging.warning(f"Non-numeric value is present in {i}th column")
        return
  columns = len(df.columns)
  weights=weights
  if ',' not in weights:
    logging.error("Weights must be separated by ','")
    return
  try:
    weights=pd.to_numeric(weights.split(','))
  except ValueError:
    logging.error("Non numeric values present in weights")
    return
      
  impact=impact
  if ',' not in impact:
    logging.error("Impacts must be separated by ','")
    return
  impact = impact.split(',')
  for i in impact:
    if i!='+' and i!='-':
      logging.error("Impact must contain '+' or '-'")
      return
  if columns-1!=len(weights) and columns-1!=len(impact):
      logging.error("Number of weights or impacts are not same as number of columns")
      return

# Helper functions
def normalised(col):
  summ=0
  for i in col:
    summ=summ+(i**2)
  summ=np.sqrt(summ)
  return summ

def weighted(df,weights):
  w=0
  for i in df.columns:
    df[i]=df[i]*int(weights[w])
    w+=1
  return df

def best(df,impact):
  c=0
  best=[]
  for i in df.columns:
    if(impact[c]=='+'):
        best.append(df[i].max())
    
    elif(impact[c]=='-'):
        best.append(df[i].min())
      
    else:
        print('wrong symbol')
    c+=1
  return (best)

def worst(df,impact):
  c=0
  worst=[]
  for i in df.columns:
    if(impact[c]=='+'):
        worst.append(df[i].min())
    elif(impact[c]=='-'):
        worst.append(df[i].max())
    else:
        print('wrong symbol')
    c+=1
  return (worst)


def euclidean_dist(df,arr):
  dist=[]
  for i in range(df.shape[0]):
    dist.append(np.sqrt((np.sum((df.iloc[i]-arr)**2))))
  return dist

def topsis_score(filename,weight,impacts,output):
    # Adding the validation for parameters.
    checkParameters(filename,weight,impacts)

    # Actual logic for topsis
    weights=list(weight.split(","))
    impact=list(impacts.split(","))
    df=pd.read_csv(filename) 
    df1=df.copy()
    df=pd.DataFrame(df)
    df.drop(columns = df.columns[0], axis = 1, inplace= True)
    for i in df.columns:
      df[i]=df[i]/normalised(df[i])
    weighted(df,weights) 
    b=best(df,impact)
    w=worst(df,impact)
    dist_pos=euclidean_dist(df,b)
    dist_neg=euclidean_dist(df,w)

    new=[]
    for i in range (len(dist_pos)):
      new.append(dist_pos[i]+dist_neg[i])

    # Formatting the output file
    df1['score']=new
    df1['score']=(dist_neg/df1['score'])
    df1['score']=(df1['score'])*100
    df1['Rank'] = (df1['score'].rank(method='max', ascending=False))
    df1['Rank']=df1['Rank'].astype(int)
    df1.to_csv(output)
