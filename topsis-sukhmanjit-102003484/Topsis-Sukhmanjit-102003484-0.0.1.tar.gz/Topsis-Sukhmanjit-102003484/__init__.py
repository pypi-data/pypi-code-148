import argparse
import os.path
from numpy import char
import pandas as pd
import math
from pandas.api import types
from pandas.api.types import is_numeric_dtype
import sys
import numpy as np

# Reference : https://www.geeksforgeeks.org/binary-search/
def binarySearch(arr, l, r, x):
 
    # Check base case
    if r >= l:
 
        mid = l + (r - l) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
 
        # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] < x:
            return binarySearch(arr, l, mid-1, x)
 
        # Else the element can only be present
        # in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)
 
    else:
        # Element is not present in the array
        return -1


#Taking input as command line arguments using argparse module
#Reference to understand : https://docs.python.org/3/howto/argparse.html#id1
parser = argparse.ArgumentParser()
parser.add_argument("InputFileName", help="Enter name of the input file")
parser.add_argument("Weights", help="Enter weights of the criterion")
parser.add_argument("Impacts", help="Enter '+' for maximizing the criteria and '-' for minimizing the criteria")
parser.add_argument("ResultFileName", help="Enter the name of file you want the result to be pushed in")
args = parser.parse_args()
input = args.InputFileName
result = args.ResultFileName

#Checking if inputfile exists or not
#Reference : https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/#:~:text=The%20is_file()%20method%20checks,the%20file%20doesn't%20exist.&text=Since%20the%20example.,is_file()%20method%20returns%20True%20.

checkfile = os.path.isfile(input)
if (checkfile == False):
    sys.exit("File not Found") # This line exits the code abruptly if condition is not followed

#Reading csv file using Pandas
df = pd.read_csv("102003484-data.csv")

#Checking whether number of columns are more than 3 or not
col = len(df.columns)
if(col<=3):
    sys.exit("Not enough columns")


#Checking whether all columns except first one are of numeric data type or not
#Used pandas submodule api.types 
#Reference : https://stackoverflow.com/questions/19900202/how-to-determine-whether-a-column-variable-is-numeric-or-not-in-pandas-numpy
for i in range(1,col):
    if(pd.api.types.is_numeric_dtype(df.iloc[:,i])== False):
        sys.exit("Non numeric data types")

#Manipulating commma separted command line arguments
#Reference : https://www.tutorialspoint.com/How-would-you-make-a-comma-separated-string-from-a-list-in-Python
weights = list(map(int, args.Weights.split(',')))
impacts = list(map(str, args.Impacts.split(',')))
impacts[0] = '-'
# # print(impacts)

# Checking whether number of weights and impacts given is equal to the number of colums
if(col!=len(weights)+1):
    sys.exit("Number of weights is not equal to number of columns")
if(col!=len(impacts)+1):
    sys.exit("Number of impacts is not equal to number of columns")

#Checking if there are any other symbols besides + or - in impacts
for i in impacts:
    if(i!='+' and i!='-'):
        sys.exit("Only + and - are allowable characters in impacts")

#-------------Topsis--------------#

#Taking all numberical columns and storing them in a new dataframe
df1 = df.iloc[:,1:]

#Using apply function to calculate square of each element and adding them together
#Reference : https://thispointer.com/pandas-apply-apply-a-function-to-each-row-column-in-dataframe/
sq_cols = df1.apply(lambda x: x*x)
sum_cols = sq_cols.apply(np.sum)


#Diving each elements by square root of sum of squares
#This step is known as normalization
j=0
for i in sum_cols:
    df1.iloc[:,j]=df1.iloc[:,j]/math.sqrt(i)
    j+=1
j=0
# # print(df1)

#Multiplying column values by their respective weights
for i in weights:
    df1.iloc[:,j]=df1.iloc[:,j]*i
    j+=1

#Calculating maximum and minimum of each column
#Reference : https://www.geeksforgeeks.org/find-maximum-values-position-in-columns-and-rows-of-a-dataframe-in-pandas/

maxClm = df1.max()
minClm = df1.min()
# # print(maxClm)
# # print(minClm)


#Now calculating the best and worst values in a column according to the given impacts
worst_val=list()
best_val=list()
j=0
for i in impacts:
    if(i=='+'):
        best_val.append(maxClm[j])
        worst_val.append(minClm[j])
    else:
        best_val.append(minClm[j])
        worst_val.append(maxClm[j])
    j+=1
# # print(best_val)
# # print(worst_val)


#Calculcating euclidean distance of each row from best and worst values
distpos = list()
distneg = list()
for k in range(0,len(df1)):
    pval = 0
    nval = 0
    for i in range(0,len(df1.columns)):
        pval += (best_val[i]-df1.iloc[k,i])**2
        nval += (worst_val[i]-df1.iloc[k,i])**2
    distpos.append(math.sqrt(pval))
    distneg.append(math.sqrt(nval))
# # print(distpos)
# # print(distneg)


#Topsis score is caculated by adding adding best and worst eulidean distances calculated above
topsis_score = list()
sorted_topsis_score = list()
for i in range(0,len(df1)):
    val = distneg[i]/(distpos[i]+distneg[i])
    topsis_score.append(val)
# #print(topsis_score)


#Using topsis score calculating ranks 

sorted_topsis_score = sorted(topsis_score) # Here i have used sorted() instead of sort() because sort() function will also change the original topsis score list as well
sorted_topsis_score.reverse()
#Using sorted will created a copy of sorted topsis score which i stored in another list
#Reference : https://stackoverflow.com/questions/13573507/how-can-i-get-a-sorted-copy-of-a-list


# # print(sorted_topsis_score)

rank = list()
for i in range(0,len(topsis_score)):
    rank.append(binarySearch(sorted_topsis_score,0,len(sorted_topsis_score)-1,topsis_score[i])+1) # I have used binary search on the sorted list to calculate ranks
# # print(rank)

#Adding two columns to the dataframe
#Reference : https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/

df["Topsis Score"] = topsis_score
df["Rank"] = rank
print("Successful!!!")
print("File saved")
for i in range(0,70):
    print("-",end="")#printing without newline in python 
#Reference : https://www.geeksforgeeks.org/print-without-newline-python/
print()
print(df)

# Saving this dataframe to the result csv file provided above
# Reference :https://www.geeksforgeeks.org/saving-a-pandas-dataframe-as-a-csv/
df.to_csv(result)



