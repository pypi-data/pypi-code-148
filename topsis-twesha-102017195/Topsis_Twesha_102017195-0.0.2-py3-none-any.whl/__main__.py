import pandas as pd
import os
# OS module in Python provides functions for interacting with the operating system.
import sys

# A header is a block of comments at the top of the code, which includes the filename, author, date, 
# and a few other details of the file and the contents of that file.
name = "Topsis_Apurvi"
__version__ = "0.0.2"
__author__ = 'Apurvi'
__credits__ = 'Thapar Institute of Engineering and Technology'


def main():
    # Arguments not equal to 5
    # print("Checking for Errors...\n")
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

# os.path module is submodule of OS module in Python used for common pathname manipulation.

    # File Not Found error
    # os.path.isfile() method in Python is used to check whether the specified path is an existing regular file or not.
    # this returns true if file exist
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    # split the path name into a pair root and ext
    # This method returns a tuple that represents root and ext part of the specified path name.
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        temp_dataset = pd.read_csv(sys.argv[1])
        nCol = len(temp_dataset.columns.values)

        # less then 3 columns in input dataset
        if nCol < 3:
            print("ERROR : Input file have less than 3 columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, nCol):
            pd.to_numeric(temp_dataset.iloc[:, i], errors='coerce')
            temp_dataset.iloc[:, i].fillna((temp_dataset.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if nCol != len(weights)+1 or nCol != len(impact)+1:
            print(
                "ERROR : Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        
        topsis_pipy(temp_dataset, nCol, weights, impact)


def Normalize(temp_dataset, nCol, weights):
    # normalizing the array
    # print(" Normalizing the DataSet...\n")
    for i in range(1, nCol):
        temp = 0
        for j in range(len(temp_dataset)):
            temp = temp + temp_dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_dataset)):
        # Pandas iat[] method is used to return data in a dataframe at the passed location.
            temp_dataset.iat[j, i] = (temp_dataset.iloc[j, i] / temp)*weights[i-1]
    return temp_dataset


def Calc_Values(temp_dataset, nCol, impact):
    # print(" Calculating Positive and Negative values...\n")
    p_sln = (temp_dataset.max().values)[1:]
    n_sln = (temp_dataset.min().values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
    return p_sln, n_sln


def topsis_pipy(temp_dataset, nCol, weights, impact):
    # normalizing the array
    temp_dataset = Normalize(temp_dataset, nCol, weights)

    # Calculating positive and negative values
    p_sln, n_sln = Calc_Values(temp_dataset, nCol, impact)

    # calculating topsis score
    # print(" Generating Score and Rank...\n")
    score = []
    for i in range(len(temp_dataset)):
        temp_p, temp_n = 0, 0
        for j in range(1, nCol):
            temp_p = temp_p + (p_sln[j-1] - temp_dataset.iloc[i, j])**2
            temp_n = temp_n + (n_sln[j-1] - temp_dataset.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    temp_dataset['Topsis Score'] = score

    # calculating the rank according to topsis score
    temp_dataset['Rank'] = (temp_dataset['Topsis Score'].rank(method='max', ascending=False))
    temp_dataset = temp_dataset.astype({"Rank": int})

    # Writing the csv
    # print(" Writing Result to CSV...\n")
    temp_dataset.to_csv(sys.argv[4], index=False)


if __name__ == "__main__":
   main()