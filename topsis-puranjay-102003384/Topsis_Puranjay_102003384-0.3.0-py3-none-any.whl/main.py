#Submission by: Puranjay Singh, 102003384(3COE9)
import pandas as pd
from tabulate import tabulate
import sys
from os import path
import math as m

class Topsis:
    def __init__(self, filename, weights, impacts, resultFileName):
        self.filename = filename.lower()
        self.weights = weights.split(",")
        self.impacts = impacts.split(",")
        self.resultFileName = resultFileName.lower()
        if ".csv" not in self.resultFileName:
            print(".csv is missing from the name of the result file!!")
            return
        if path.exists(self.filename) :
            if len(self.weights) == len(self.impacts):
                self.topsis()
            else :
                print("ERROR!!No. of weights and impacts should be equal.")
                return
        else :
            print("ERROR!!Input file doesn't exist.")
            return
            
    def topsis(self):
        self.weights = [int(w) for w in self.weights]
        dataset = pd.read_csv(self.filename)
        dataset.dropna(inplace = True)
        d = dataset.iloc[0:,1:].values
        matrix = pd.DataFrame(d)

        if len(matrix.columns) != len(self.weights) and len(matrix.columns) != len(self.impacts):
            print("ERROR!!No. of weights and impacts incorrect.")
            exit()
        sumOfSquares = []
        for col in range(0, len(matrix.columns)):
            X = matrix.iloc[0:,[col]].values
            sum = 0
            for value in X:
                sum = sum + m.pow(value, 2)
            sumOfSquares.append(m.sqrt(sum))
        j = 0
        while(j < len(matrix.columns)):
            for i in range(0, len(matrix)):
                matrix[j][i] = matrix[j][i]/sumOfSquares[j] 
            j = j+1
        k = 0
        while(k < len(matrix.columns)):
            for i in range(0, len(matrix)):
                matrix[k][i] = matrix[k][i]*self.weights[k] 
            k = k+1
        bestValue = []
        worstValue = []
        for col in range(0, len(matrix.columns)):
            Y = matrix.iloc[0:,[col]].values
            if self.impacts[col] == "+" :
                maxValue = max(Y)
                minValue = min(Y)
                bestValue.append(maxValue[0])
                worstValue.append(minValue[0])
            if self.impacts[col] == "-" :
                maxValue = max(Y)
                minValue = min(Y)
                bestValue.append(minValue[0])
                worstValue.append(maxValue[0])
        SiPlus = []
        SiMinus = []
        for row in range(0, len(matrix)):
            temp = 0
            temp2 = 0
            wholeRow = matrix.iloc[row, 0:].values
            for value in range(0, len(wholeRow)):
                temp = temp + (m.pow(wholeRow[value] - bestValue[value], 2))
                temp2 = temp2 + (m.pow(wholeRow[value] - worstValue[value], 2))
            SiPlus.append(m.sqrt(temp))
            SiMinus.append(m.sqrt(temp2))
        Pi = []
        for row in range(0, len(matrix)):
            Pi.append(SiMinus[row]/(SiPlus[row] + SiMinus[row]))
        Rank = []
        sortedPi = sorted(Pi, reverse = True)
        for row in range(0, len(matrix)):
            for i in range(0, len(sortedPi)):
                if Pi[row] == sortedPi[i]:
                    Rank.append(i+1)
        col1 = dataset.iloc[:,[0]].values
        matrix.insert(0, dataset.columns[0], col1)
        matrix['Topsis Score'] = Pi
        matrix['Rank'] = Rank
        newColNames = []
        for name in dataset.columns:
            newColNames.append(name)
        newColNames.append('Topsis Score')
        newColNames.append('Rank')
        matrix.columns = newColNames
        matrix.to_csv(self.resultFileName)
        print(tabulate(matrix, headers = matrix.columns))

def main():
    if len(sys.argv) != 5:
        print("ERROR!!Invalid number of arguments.")
        exit()
    Topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
if __name__ == "__main__":
    main()
