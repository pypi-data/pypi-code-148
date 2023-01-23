import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 5:
        print("Arguments missing or not provided properly.\n Required input format- python <script_name> <input_data_file_name> <wt> <imp> <result_file_name>")
        exit()

    inputFile = sys.argv[1]
    weight = sys.argv[2]
    impact = sys.argv[3]
    outputFile = sys.argv[4]

    try:
        df = pd.read_csv(inputFile)
    except FileNotFoundError:
        print("File NOT found in the given location")
        exit()

    df1 = df.copy()

    if len(df.columns) < 3:
        print("Not sufficient number of columns. Number of columns should be greater than or equal to 3")
        exit()

    for col in df.columns[1:]:
        if np.issubdtype(df[col].dtype, np.number)==np.False_:
            print("Non numerical value found")
            exit()

    imp = impact.split(sep=',')
    w = weight.split(sep=',')

    if len(imp) != len(df.columns)-1 or len(w) != len(df.columns)-1:
        print("Invalid number of weights or impacts")
        exit()
    for i in imp:
        if i != "+" and i != "-":
            print("Invalid impact!!!")
            exit()
    w1 = []
    for i in w:
        try:
            w1.append(float(i))
        except:
            print("Invalid weight")
            exit()

    for col in df.columns[1:]:
        df[col] = df[col]/(sum(pow(pow(df[col],2)),0.5))

    for i in range(len(w1)):
        df.iloc[:, i+1] = df.iloc[:, i+1]*w1[i]

    p = []
    n = []

    for i in range(len(imp)):
        if imp[i] == '+':
            p.append(max(df.iloc[:, i+1]))
            n.append(min(df.iloc[:, i+1]))
        else:
            p.append(min(df.iloc[:, i+1]))
            n.append(max(df.iloc[:, i+1]))

    sp = []
    sn = []

    for i in range(len(df)):
        sp.append((sum(pow(pow(df.iloc[i, 1:]-p),2)),0.5))
        sn.append((sum(pow(pow(df.iloc[i, 1:]-n),2)),0.5))

    score = []

    for i in range(len(sp)):
        score.append(sn[i]/(sp[i]+sn[i]))

    df['Score'] = score

    df1['Topsis Score'] = score
    df1['Rank'] = df['Score'].rank(ascending=False)
    print(df1)
    df1.to_csv(outputFile, index=False)

if __name__ == "__main__":
    main()