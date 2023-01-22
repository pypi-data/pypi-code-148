import pandas as pd
import numpy as np
import sys

def main():
    # Error Handling
    if len(sys.argv)!=5:
        sys.exit('Wrong number of arguments provided (pls provide 4)')
    if len(sys.argv)>2:
        try:
            df = pd.read_csv(sys.argv[1])
        except FileNotFoundError as e:
            print(f"FileNotFoundError successfully handled\n"f"{e}")
    else:
        df = pd.read_csv('102017040-data.csv')

    print(df)
    m = len(df)
    n = len(df.axes[1])-1
    if n<=2:
        sys.exit('The provided file does not have sufficient columns!')
    vals = df.iloc[:,1:n+1].values 
    if len(sys.argv) < 5:
        # For Debugging
        weights = [0.25 for i in range(n)]
        impact = ['-','+','+','+','+']
    else:
        try:
            weights = list(map(float,sys.argv[2].split(',')))
            impact = list(map(str,sys.argv[3].split(',')))
        except:
            sys.exit("Please enter the correct values as the arguments and use commas to seperate the weights and the impacts")

    for i in range(len(impact)):
        if impact[i] != '+' and impact[i] != '-':
            sys.exit("Please enter only '+' or '-' in impact(3rd argument)")

    if (n != len(impact)) or (len(impact) != len(weights)):
        sys.exit('Length of weight and length of impact should be equal to number of columns')

    sq_sum = [0 for i in range(n)]
    colmax = [0 for i in range(n)]
    colmin = [0 for i in range(n)]
    for i in range(n):
        temp_sum = 0
        for j in range(m):
            temp_sum += vals[j][i]**2

        sq_sum[i] = temp_sum**0.5

    vals = np.array(vals,dtype=float)

    for i in range(n):
        cmax = (vals[0][i]/sq_sum[i])*weights[i]
        cmin = cmax
        for j in range(m):
            vals[j][i] = (vals[j][i]/sq_sum[i])*weights[i]
            if cmax < vals[j][i]:
                cmax = vals[j][i]
            if cmin > vals[j][i]:
                cmin = vals[j][i]

        if impact[i] == '+':
            colmax[i] = cmax 
            colmin[i] = cmin
        else:
            colmax[i] = cmin
            colmin[i] = cmax


    p = [0 for i in range(m)]
    for i in range(m):
        vpls = 0
        vmin = 0
        for j in range(n):
            vpls += (vals[i][j]-colmax[j])**2
            vmin += (vals[i][j]-colmin[j])**2

        vpls = vpls**0.5
        vmin = vmin**0.5
        p[i] = vmin/(vpls+vmin)

    df['Topsis Score'] = p
    df['Rank'] = df['Topsis Score'].rank(method='max',ascending=False)
    df['Rank'] = df['Rank'].astype('int')

    print(df)
    if len(sys.argv) >=5:
        try:
            df.to_csv(sys.argv[4],index=False)
        except:
            sys.exit('File not written due to error')


if __name__ ==  '__main__':
    main()