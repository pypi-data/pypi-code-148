# Samarjot Singh      102003242

import sys
import pandas as pd
import numpy as np
import math as m


def main():
    if len(sys.argv) < 5:
        print('Insufficient arguments passed in CLI. Exiting!!!')
        sys.exit()

    fname = sys.argv[1]
    w = sys.argv[2]
    im = sys.argv[3]
    rfname = sys.argv[4]

    w = list(map(float, w.split(',')))
    im = list(map(str, im.split(',')))

    ds = pd.read_csv(fname)
    data = ds.iloc[ :, 1:].values.astype(float)
    (r,c) = data.shape
    s = sum(w)

    if len(w) != c:
        print("Insufficient weight values. Exiting!!!")
        sys.exit()

    for i in range(c):
        w[i] /= s

    a = [0]*(c)

    for i in range(0, r):
        for j in range(0, c):
            a[j] = a[j]+(data[i][j]*data[i][j])

    for j in range(c):
        a[j] = m.sqrt(a[j])

    for i in range(r):
        for j in range(c):
            data[i][j] /= a[j]
            data[i][j] *= w[j]

    # print(data)
    df = pd.DataFrame(data)
    df.to_csv(rfname)

    p_ideal = np.amax(data, axis = 0)
    n_ideal = np.amin(data, axis = 0)
    for i in range(len(im)):
        if(im[i] == '-'):
            temp = p_ideal[i]
            p_ideal[i] = n_ideal[i]
            n_ideal[i] = temp

    p_dist = list()
    n_dist = list()

    for i in range(r):
        s = 0
        for j in range(c):
            s += pow((data[i][j]-p_ideal[j]), 2)

        p_dist.append(float(pow(s, 0.5)))

    for i in range(r):
        s = 0
        for j in range(c):
            s += pow((data[i][j]-n_ideal[j]), 2)

        n_dist.append(float(pow(s, 0.5)))

    p_score = dict()

    for i in range(r):
        p_score[i+1] = n_dist[i]/(n_dist[i]+p_dist[i])

    a = list(p_score.values())
    b = sorted(list(p_score.values()), reverse = True)
    rank = dict()

    for i in range(len(a)):
        rank[(b.index(a[i]) + 1)] = a[i]
        b[b.index(a[i])] =- b[b.index(a[i])]

    row = list(i+1 for i in range(len(b)))
    a = list(rank.values())
    rr = list(rank.keys())

    out = {'Row No.':row, 'Performance Score' : a, 'Rank':rr}
    output = pd.DataFrame(out)
    print(output)

if __name__=="__main__":
    main()