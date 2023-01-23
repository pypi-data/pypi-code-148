import pandas as pd
import sys
import os
import math

try:
    def main():
        if not os.path.exists(datafile):
            raise Exception('File not Found')
        if len(sys.argv) != 5:
            raise Exception('Usage python <program.py> <InputDataFile.csv> <Weights> <Impacts> <output.csv>')


        datafile = sys.argv[1]
        weights = sys.argv[2].split(',')
        impacts = sys.argv[3].split(',')
        outputfile = sys.argv[4]



        df = pd.read_csv(datafile)
        if len(df.columns) < 3:
            raise Exception('Input file must contain 3 or more columns')

        col_names = list(df.columns[1:])
        for i in col_names:
            if not df[i].apply(lambda x: isinstance(x, (int,float))).all():
                raise Exception('Value not numeric')

        if len(col_names) != len(weights) or len(col_names) != len(impacts):
            raise Exception('Lengths of weights and impacts must be same as that of columns')

        for i in impacts:
            if not i in ['+','-']:
                raise Exception('Impacts can only be + or -')

        col_sum = df.iloc[:,1:].apply(lambda x: math.sqrt(x.pow(2).sum()))

        for i,col in enumerate(col_names):
            df[col] = df[col] / col_sum[i] * float(weights[i])
        v_pos = []
        v_neg = []
        for i,col in enumerate(col_names):
            if impacts[i] == '+':
                v_pos.append(df[col].max())
                v_neg.append(df[col].min())
            else:
                v_neg.append(df[col].max())
                v_pos.append(df[col].min())

        s_pos = df.iloc[:,1:].apply(lambda x: math.sqrt(((x-v_pos)**2).sum()), axis=1)
        s_neg = df.iloc[:,1:].apply(lambda x: math.sqrt(((x-v_neg)**2).sum()), axis=1)

        df['Topsis Score'] = s_neg / (s_neg + s_pos)

        df['Rank'] = df['Topsis Score'].rank(ascending=0).astype(int)

        df.to_csv(outputfile, index=False)


    if __name__ == '__main__':
        main()

except Exception as e:
    print(e)
