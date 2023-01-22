import pandas as pd
import os
import sys


def topsis():
    # Arguments not equal to 5
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dataset, temp_dataset = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        nCol = len(temp_dataset.columns.values)

        # less then 3 columns in input dataset
        if nCol < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, nCol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

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
        topsis_fun(temp_dataset, dataset, nCol, weights, impact)

def Normalize(dataset, nCol, weights):
    for i in range(0, nCol):
        temp = 0
        for j in range(len(dataset)):
            temp += dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(dataset)):
            dataset.iat[j, i] = (
                dataset.iloc[j, i] / temp)*weights[i-1]
    return dataset


def func(dataset, nCol1, impact):
    positive = (dataset.max().values)[0:]
    negative = (dataset.min().values)[0:]
    for i in range(0, nCol1):
        if impact[i] == '-':
            positive[i] = negative[i]
            negative[i] = positive[i]
    return positive, negative


def topsis_fun(temp,data,nCol, weights, impact):
    ##remove 1st column which is the name column
    data.drop(data.columns[0], axis=1, inplace=True)
    nCol1=len(data.columns)
    temp = Normalize(data, nCol1, weights)

    # Calculating positive and negative values
    positive, negative = func(temp, nCol1, impact)

    score = []
    for i in range(len(data)):
        temp_p= 0
        temp_n=0
        for j in range(0, nCol1):
            temp_p = temp_p + (positive[j] - data.iloc[i, j])**2
            temp_n = temp_n + (negative[j] - data.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    data['Score'] = score

    # calculating the rank according to topsis score
    data['Rank'] = (data['Score'].rank(
        method='max', ascending=False))
    data = data.astype({"Rank": int})
    data.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    topsis()

