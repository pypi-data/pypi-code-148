from inspect import EndOfBlock
import numpy as np
import pandas as pd
import sys
import csv

def topsis(data, weights, impact):
    try:
        # Normalizing the data and forming the normalized decision matrix
        data = data / np.linalg.norm(data, axis=0)
        data = data*weights*impact
        # Calculate the ideal solutions(the ideal best and ideal worst solutions)
        ideal_best = np.max(data,axis=0)
        ideal_worst = np.min(data,axis=0)

        # Calculate the relative closeness to the ideal solution
        eucledian1 = np.sqrt(np.sum((data - ideal_best) ** 2, axis=1))
        eucledian2 = np.sqrt(np.sum((data - ideal_worst) ** 2, axis=1))
        perf_score=eucledian2/(eucledian1+eucledian2)
            
        return perf_score
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def main():
    try:
        # Read input file name from command line
        input_file = sys.argv[1] 
        # Read data from CSV file
        data = pd.read_csv(input_file,skiprows=0,index_col=0).values
        if(len(data[0])<2):
          print("Too less number of columns!!Add more data")
          sys.exit(1)
        
        # Reading weights and impacts from command line arguments
        weights = list(map(float, sys.argv[2].split(',')))
        impact = list(map(str, sys.argv[3].split(',')))
        if(len(weights)!=len(impact) or len(weights)!=len(data[0]) or len(impact)!=len(data[0])):
          print("Lengths of impact and weight must be equal to number of columns.")
          sys.exit(1)
        for i in range(0,len(impact)):
          if(impact[i]=="+"):
            impact[i]=1
          elif (impact[i]=="-"):
            impact[i]=-1
          else:
            print("Incorrect syntax for impacts.") 
            sys.exit(1)
           
          
        
        perf_score = topsis(data, weights, impact)
        if perf_score is not None:
            # Writing the output to a new csv file and appending it with the original csv input file.
            np.savetxt(sys.argv[4], perf_score, delimiter=",",header="Topsis Score",comments="")
            df1=pd.read_csv(sys.argv[1])
            df=pd.read_csv(sys.argv[4])
            df = df.assign(Rank=df['Topsis Score'].rank(ascending=False))
            df3=df1.join(df)
            df3.to_csv(sys.argv[4],index=False)
            print("Output file generated successfully")
        else:
            print("An error occurred.")
    except Exception as e:
        print("An error occurred:", e)

if __name__=='__main__':
  main()