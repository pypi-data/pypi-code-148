import pandas as pd
import numpy as np
import os
import sys


def main():
    # Arguments not equal to 5
    # print("Checking for Errors...\n")
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
        # print(" No error found\n\n Applying Topsis Algorithm...\n")
        topsis_pipy(temp_dataset, dataset, nCol, weights, impact)

def topsis_pipy(temp_dataset, dataset, nCol, weights, impact):
    # normalizing the array
    # temp_dataset = Normalize(temp_dataset, nCol, weights)
    ndf = temp_dataset.drop('Fund Name', axis=1)
    row = len(ndf)
    cols = len(ndf.iloc[0,:])

    den= ndf.apply(np.square).apply(np.sum,axis = 0).apply(np.sqrt)
    for i in range(cols):
        for j in range(row):
            ndf.iat[j, i] = (ndf.iloc[j, i] / den[i]) * weights[i]

    ideal_best = (ndf.max().values)
    ideal_worst = (ndf.min().values)
    for i in range(cols):
        if impact[i] == '-':
            ideal_best[i], ideal_worst[i] = ideal_worst[i], ideal_best[i]

    score = []
     # Calculating positive and negative values
    for i in range(row):
        p,n = 0, 0
        for j in range(cols):
            p += (ideal_best[j] - ndf.iloc[i, j])**2
            n += (ideal_worst[j] - ndf.iloc[i, j])**2
        p, n = p*0.5, n*0.5
        score.append(n/(p + n))

    # calculating topsis score
   
    dataset['Topsis Score'] = score

    # calculating the rank according to topsis score
    dataset['Rank'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})

    # Writing the csv
    # print(" Writing Result to CSV...\n")
    dataset.to_csv(sys.argv[4], index=False)
    # print(" Successfully Terminated")


if __name__ == "__main__":
    main()

