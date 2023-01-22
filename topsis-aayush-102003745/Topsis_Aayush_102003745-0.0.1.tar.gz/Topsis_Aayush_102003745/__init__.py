import numpy as np
import pandas as pd
import math
import copy
import os, sys

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
        dataset_2 = dataset.to_numpy()
        weights = np.array(weights)

        topsis(dataset_2, weights, impact)  


        

def topsis(mat, w , impact):

    l1 = ['M1','M2','M3', 'M4', 'M5', 'M6', 'M7', 'M8']

    p1 = mat[:,1]    
    p2 = mat[:,2]   
    p3 = mat[:,3]   
    p4 = mat[:,4]   
    p5 = mat[:,5]   
    mat_2 = []
    #print(mat)
    mat = np.delete(mat, 0, 1)
    n = mat.shape[0]
    m = mat.shape[1]
    var = mat.transpose(1, 0)
    #print(mat.shape)
    for i in range(m):
        var_2 = copy.deepcopy(var[i])
        var_3 = copy.deepcopy(var[i])
        #print(var_2)
        
        for j in range(n):
            var_2[j] = var_2[j]**2
            
        val = np.sum(var_2)
        val_2 = math.sqrt(val)
        var_3 = (var_3/(val_2))*w[i]  # multiply weight
           
        v_j = max(var_3)
        v_i = min(var_3)
        
        mat_2.append(var_3)
     
    mat_2 = np.matrix(mat_2)
 
    mat_2.transpose(1,0)   
    mat = np.array(mat_2)

    val_2 = np.amax(mat.transpose(1,0), axis = 0)    # the maximum value in each column a list
    val_3 = np.amin(mat.transpose(1,0), axis = 0)    # the minimum value in each column a list
    
    val_2 = np.array(val_2)
    val_3 = np.array(val_3)
    
    val2_len  = len(val_2)
   
    ideal_best = []
    ideal_worst = [] 
       
    for i in range(val2_len):
        if impact[i] == '+':
            ideal_best.append(val_2[i])
            ideal_worst.append(val_3[i])
        else :
            ideal_best.append(val_3[i])
            ideal_worst.append(val_2[i])
           
    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)
              
    si_plus = []
    si_minus = []
    p_i = []
    val_i = []
    
    mat = mat.transpose(1,0)
    for i in range(mat.shape[0]):
        sum_plus = 0
        sum_minus = 0
        for j in range(mat.shape[1]):
            
            value_plus = ((mat[i][j] - ideal_best[j])**2)
            
            value_minus = ((mat[i][j] - ideal_worst[j])**2)
            
            sum_plus = sum_plus + (value_plus)
            sum_minus = sum_minus + (value_minus)
            
        si_plus.append(math.sqrt(sum_plus))
        si_minus.append(math.sqrt(sum_minus))
        p_i.append(math.sqrt(sum_minus)/(math.sqrt(sum_plus) + math.sqrt(sum_minus)))
        val_i.append(i+1)
         
    si_plus = np.array(si_plus)
    si_minus = np.array(si_minus)
    p_i = np.array(p_i)
    val_i = np.array(val_i)
    
    a_1 = np.hstack((si_plus, si_minus))
    
    a_2 = np.hstack((p_i, val_i))
    a_3 = np.hstack((a_1,a_2))
    a_3 = a_3.reshape((m-1,n))
    a_3 = a_3.transpose(1,0)
       
    perf_rank1 = []
    
    for i in range(n):
        perf_rank1.append(a_3[i][3])
       
    perf_rank1 = np.array(perf_rank1)
    temp = perf_rank1.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(perf_rank1))
    
    a_6 = pd.DataFrame(a_3)
    a_7 = a_6.sort_values(by = 2 , ascending = False)
    rank = []
    for i in range(n):
        rank.append(i+1)
    a_7['rank'] = rank
    a_7.drop(a_7.columns[[0, 1]], axis=1, inplace=True)
    a_7 = a_7.sort_values(by = 3 )
    #a_7.drop(a_7.columns[[3]], axis=1, inplace=True)
    #print(a_7)
    p6 = [p1, p2, p3, p4, p5]
    p6 = np.asmatrix(p6)
    p6 = p6.T

    a_8 = pd.DataFrame(p6)
    #print(a_8)
    a_9 = pd.concat([a_7, a_8], axis=1, join='inner')
    a_9.set_axis(['Topsis Score', 'Index', 'Rank', 'P1','P2','P3','P4','P5'], axis='columns', inplace=True)
    a_9.drop('Index', axis=1, inplace=True)
    #a_9.set_axis(l1, axis='rows', inplace=True)
    #print(a_9)
    a_9['Fund name'] = l1
    #print(a_9)
    a_10 = a_9[['Fund name','P1','P2','P3','P4','P5','Topsis Score','Rank']]
    print(a_10)
    
    a_10.to_csv(sys.argv[4], index = False)




                                                                                                                                                                                                                                                                                  
    
# mat_m = np.array([250,16,12,5,200,16,8,3,300,32,16,4,275,32,8,4,225,16,16,2])
# mat_m = mat_m.reshape((5,4))
# w_m = np.array([0.25, 0.25, 0.25, 0.25])
# impact_m = ['-','+','+','+']

# topsis(mat_m,w_m,impact_m)
if __name__ == "__main__" :  
    main()
