import pandas as pd
import sys
import math

# author : Sahil Chhabra
# email : sahil.chh718@gmail.com


def main():
    try:
        read_file = pd.read_csv(sys.argv[1])
        print(sys.argv)
        df = pd.DataFrame(read_file)
        df1 = df.drop(df.columns[0], axis=1)
        w = sys.argv[2]
        weight = w.split(",")
        weight = [eval(i) for i in weight]
        i = sys.argv[3]
        impact1 = i.split(",")
        impact = []
        for i in impact1:
            if i == '+':
                impact.append(1)
            elif (i == '-'):
                impact.append(0)
        # print(impact)
        rows = df1.shape[0]
        cols = df1.shape[1]
        ss = []
        for j in range(0, cols):
            sum = 0
            for i in range(0, rows):
                sum = sum+(df1.iloc[i, j]*df1.iloc[i, j])
            sum = math.sqrt(sum)
            ss.append(sum)
        # print(ss)

        for j in range(0, cols):
            for i in range(0, rows):
                df1.iloc[i, j] = (df1.iloc[i, j]/ss[j])*weight[j]
        best = []
        worst = []
        for j in range(0, cols):
            max = -1
            min = 10000
            for i in range(0, rows):
                if (df1.iloc[i, j] > max):
                    max = df1.iloc[i, j]
                if (df1.iloc[i, j] < min):
                    min2 = df1.iloc[i, j]
            if (impact[j] == 1):
                best.append(max)
                worst.append(min)
            elif (impact[j] == 0):
                best.append(min)
                worst.append(max)
        ed_b = []
        ed_w = []
        for i in range(0, rows):
            sum_b = 0
            sum_w = 0
            for j in range(0, cols):
                sum_b = sum_b+((df1.iloc[i, j]-best[j])
                               * (df1.iloc[i, j]-best[j]))
                sum_w = sum_w+((df1.iloc[i, j]-worst[j])
                               * (df1.iloc[i, j]-worst[j]))
            ed_b.append(math.sqrt(sum_b))
            ed_w.append(math.sqrt(sum_w))

        p = []
        for i in range(0, rows):
            p.append(ed_w[i]/(ed_b[i]+ed_w[i]))
        df["score"] = p
        df["Rank"] = df["score"].rank()
        df.to_csv(sys.argv[4], index=False)
    except FileNotFoundError:
        print('file not found')
    except:
        if (len(sys.argv) != 5):
            print('ERROR: Please provide four arguments')
        elif (len(weight) != len(impact) or len(weight) != cols or len(impact) != cols):
            print('ERROR: incorrect arguments')
        else:
            print('ERROR')


if __name__ == '__main__':
    main()