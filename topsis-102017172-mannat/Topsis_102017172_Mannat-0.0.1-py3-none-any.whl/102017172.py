import pandas as pd
import sys
import math
import copy

class Topsis:
    def __init__(self, data):
        self.data = data
    def topsis(self, weights, impacts):
        data_new = copy.deepcopy(self.data)
        rms = 0
        w=0
        n = len(data_new.index)
        ideal_best = []
        ideal_worst = []
        
        for i in list(data_new):
            maximum = 0
            minimum = 1
            total = 0
            for j in range(n):
                total += data_new[i][j]
            rms = math.sqrt(total)
            for k in range(n):
                data_new[i][k] = (data_new[i][k]/rms)*weights[w]
                if data_new[i][k] > maximum:
                    maximum = data_new[i][k]
                if data_new[i][k] < minimum:
                    minimum = data_new[i][k]
            if impacts[w] == "+":
                ideal_best.append(maximum)
                ideal_worst.append(minimum)
            else:
                ideal_best.append(minimum)
                ideal_worst.append(maximum)
            w+=1
            
        k = 0
        per = []
        for i in range(n):
            si_pos = math.sqrt(sum((data_new.iloc[i,:] - ideal_best)*(data_new.iloc[i,:] - ideal_best)))
            si_neg = math.sqrt(sum((data_new.iloc[i,:] - ideal_worst)*(data_new.iloc[i,:] - ideal_worst)))
            p = si_neg/(si_pos+si_neg)
            per.append([k, p])
            k+=1
            
        per.sort(key = lambda x : x[1], reverse = True)
        rank = 1
        for i in range(len(per)):
            per[i].append(rank)
            rank += 1
            
        per.sort(key= lambda x: x[0])
        
        per_score = []
        per_rank = []
        
        for i in range(len(per)):
            del per[i][0]
            per_score.append(per[i][0])
            per_rank.append(per[i][1])
            
        data_new["Topsis Score"] = per_score
        data_new["Rank"] = per_rank
        return data_new


def main():
    if len(sys.argv) != 5:
        print('''ERROR!
        Command line usage: python 102017172.py <InputFile> <Weights> <Impacts> <ResultFile>''')
        exit()

    input_file = sys.argv[1]

    df = pd.DataFrame()

    try:
        df = pd.read_excel(input_file)
    except:
        print("Input file not found")
        exit()

    weights = sys.argv[2].split(",")
    impacts = sys.argv[3].split(",")

    if len(weights) < 2 or len(impacts) < 2:
        print("Weights and impacts should be separated by ',' or be more than 2 ")
        exit()


    if(len(weights) != len(impacts)):
        print("Length of weight and impacts is not equal")
        exit()

    k = 0
    for i in impacts:
        if i not in ["+", "-"]:
            print("Impact can either be positive or negative")
            exit()
        weights[k] = int(weights[k])
        k += 1


    new_df = df.iloc[:,1:]
    name = df.iloc[:,:1]

    if len(new_df) < 2:
        print("Columns are not appropriate")
        exit()

    topsis = Topsis(new_df)
    res = topsis.topsis(weights, impacts)
    print(res)
    
    res.insert(0, "Model", name)

    result_102017172 = sys.argv[4]
    res.to_csv(f"./{result_102017172}.csv", index = False)
    
if __name__ == '__main__':
     main()