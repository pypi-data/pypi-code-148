# Name=Ikshit
# Roll_no=102003403
# Group=CO16
import pandas as pd
import sys
import os
import math

def topsis():
  try:
    # def main():
      # Exception handling
      # 1
      # Correct number of parameters (inputFileName, Weights, Impacts, resultFileName).
      if(len(sys.argv) != 5):
        raise Exception('Error,Wrong Format!!! \nExpected Format is : python <program.py> <InputDataFile.csv> <Weights> <Impacts> <output.csv>\nExiting!!!')


      data_set = sys.argv[1]
      weights = sys.argv[2].split(',')
      impacts = sys.argv[3].split(',')
      final_data_set = sys.argv[4]

      # Handling of “File not Found” exception
      if(os.path.exists(data_set)==False):
        raise Exception('Error!!!\nFile not Found!\nExiting!!!')

      # Input file must contain three or more columns.
      df = pd.read_csv(data_set)
      # print(df)
      if(len(df.columns) < 3):
        raise Exception('Warning!!!\nInput file must contain 3 or more columns\nExiting!!!')

      # From 2nd to last columns must contain numeric values only (Handling of non-numeric values)
      col = list(df.columns[1:])
      for i in col:
        for j in df[i]:
          if(isinstance(j, int)==False and isinstance(j, float)==False):
            raise Exception('Error!!!\n2nd to last columns must contain numeric values only\nExiting!!!')

      # Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same
      if(len(col) != len(weights) or len(col) != len(impacts)):
        raise Exception('Error!!!\nLengths of weights and impacts must be same as that of columns!\nExiting!!!')

      # Impacts must be either +ve or -ve.
      for i in impacts:
          if not i == '+' and not i == '-':
              raise Exception('Error!!!\nImpacts must be either +ve or -ve.\nExiting!!!')

      # Impacts and weights must be separated by ‘,’ (comma)
      seperators = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '+': True, '*': True,'-': True, '=': True}
      seperators_impact = {'.':True,'@': True, '^': True, '!': True, ' ': True, '#': True, '%': True,'$': True, '&': True, ')': True, '(': True, '*': True, '=': True}
      def char_check(new_list, seperators):
        for item in new_list:
          for char in item:
            if char in seperators:
              return False

      def string_check(comma_check_list, seperators):
        for string in comma_check_list:
          new_list = string.split(",")
          if char_check(new_list, seperators) == False:
            raise Exception("Error!!!\nImpacts and weights must be separated by ‘,’ (comma)\nExiting!!!")

      string_check(sys.argv[2], seperators)
      string_check(sys.argv[3], seperators_impact)


      # Step 2.1: Vector Normalization
      # Calculate Root of Sum of Squares
      col_sum = []
      for i in col:
        col_sum.append(math.sqrt(df[i].pow(2).sum()))

      # Step 2.2: Vector Normalization
      # Find Normalized Decision Metrix -
      # Divide every column value its Root of Sum of Squares
      count = 0
      for i in col:
        df.loc[:, i] = df.loc[:, i] / col_sum[count]

        # Step 3: Weight Assignment
        # Calculate Weight × Normalized performance value
        df.loc[:, i] = df.loc[:, i] * float(weights[count])
        count = count + 1

      # Step 4: Find Ideal Best and Ideal Worst
      v_pos = []
      v_neg = []

      count = 0
      for i in col:
        if impacts[count] == '+':
          v_pos.append(df[i].max())
          v_neg.append(df[i].min())
        else:
          v_neg.append(df[i].max())
          v_pos.append(df[i].min())
        count = count + 1

      s_pos = []
      s_neg = []

      # Step 5: Calculate Euclidean distance
      # Calculate Euclidean distance from ideal best value and ideal worst value
      for i in range(len(df)):
        count = 0
        pos_sum = 0
        neg_sum = 0
        for j in range(1, len(df.loc[i])):
          pos_sum = pos_sum + (df.iloc[i, j] - v_pos[count])*(df.iloc[i, j] - v_pos[count])
          neg_sum = neg_sum + (df.iloc[i, j] - v_neg[count])*(df.iloc[i, j] - v_neg[count])
          count = count + 1
        s_pos.append(math.sqrt(pos_sum))
        s_neg.append(math.sqrt(neg_sum))

      # Step 6: Calculate Performance Score
      performance = []
      for i in range(len(s_pos)):
          performance.append((s_neg[i]) / (s_neg[i] + s_pos[i]))
      # print(performance)
      df['Topsis Score'] = performance

      df['Rank'] = df['Topsis Score'].rank(ascending=0)
      df['Rank'] = df['Rank'].astype(int)

      df.to_csv(sys.argv[4],index=False)
      # print(df)


    # if __name__ == '__main__':
    #   main()

  except Exception as e:
    print(e)

topsis()