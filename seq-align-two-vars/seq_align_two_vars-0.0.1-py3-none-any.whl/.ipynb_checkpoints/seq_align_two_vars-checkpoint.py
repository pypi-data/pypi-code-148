import numpy as np
import pandas as pd

def sim_func_default(a,b):
    if a == b:
        return 1
    else:
        return -1
    
def sim_func(a,b):
    if a == b:
        return 1
    if a == "Medium" and b == "Female":
        return -0.5
    if a == "Female" and b == "Medium":
        return -0.5
    if a == "Minimum" and b == "Young":
        return -0.5
    if a == "Young" and b == "Minimum":
        return -0.5
    else:
        dict_security = {"Supermax": 4, "Maximum": 3, "Close": 2, "Medium": 1, "Female": 1, "Minimum": 0, "Young": 0}
        return -np.abs(dict_security[a] - dict_security[b])
    
def distance(val):
    if val > 0:
        return 0
    else:
        return -val
    
def pretty_print(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    print('\n')
    
def random(length, category):
    cate_lst = []
    time_lst = []
    dis_lst = []
    lst = [cate_lst, time_lst, dis_lst]
    for i in range(length):
        cur = category[np.random.randint(0, len(category))]
        cate_lst.append(cur)
    
    for i in range(length - 1):
        time_lst.append(np.random.rand())
        dis_lst.append(np.random.rand())
    return lst

import networkx as nx
from matplotlib import pyplot as plt

def draw(row):
    
    G=nx.DiGraph()
    security = row[2]
    time = row[3]
    dis = row[4]
    
    plt.figure(1,figsize=(2.5 * len(security),2)) 

    node_size = []
    for i in range(len(security) - 1):
        node_size.append(1000 + 10000 * float(time[i]))
    node_size.append(1000)
    node_color = []
    width = []
    sum_dis = 0
    for i in range(len(security)):
        if i == 0:
            G.add_node(i, pos = (0,1))
        elif i != len(security) - 1:
            diss = (np.sqrt(node_size[i]/31400)-np.sqrt(2000/31400) + np.sqrt(node_size[i-1]/31400)-np.sqrt(2000/31400))**2
            sum_dis = sum_dis + diss + 1
            G.add_node(i, pos = (sum_dis,1))
        else:
            G.add_node(i, pos = (sum_dis+1,1))
        if security[i] == "Supermax":
            node_color.append("r")
        if security[i] == "Maximum":
            node_color.append("y")
        if security[i] == "Close":
            node_color.append("g")
        if security[i] == "Medium" or security[i] == "Female":
            node_color.append("b")
        if security[i] == "Minimum" or security[i] == "Young":
            node_color.append("m")

    edge_labels = {}
    for i in range(len(security) - 1):
        G.add_edge(i, i+1, len= 1)
        edge_labels[(i, i+1)] = round(float(dis[i]),2)
        width.append(0.2+float(dis[i]) * 10)
    pos=nx.get_node_attributes(G,'pos')
    
    labeldict = {}
    
    for i in range(len(security) - 1):
        labeldict[i] = security[i] + "\n" + str(round(float(time[i]),2))
    labeldict[i+1] = security[i+1]
    
    nx.draw(G,pos, labels = labeldict, node_size = node_size, width = width, node_color = node_color, edge_color = 'b')
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.show()
    
def propogate_matrix_global_two_vars(X, Y, X1, Y1, X2, Y2, ratio, gap_score, align_score, proportion):
    X1.insert(0, 0)
    Y1.insert(0, 0)
    X2.insert(0, 0)
    Y2.insert(0, 0)
    
    value_matrix = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_matrix = [[[0, 0] for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_gap_score = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    need_constant_gap = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    
    need_constant_gap[0][0] = 1
    
    for j in range(len(Y)+1):
        for i in range(len(X)+1):
            if j == 0 and i == 0:
                continue
            # For the global approach, the first row and column involves the time penalties
            # of adding in a gap of a given length to the beginning of either sequence.
            elif j == 0:
                above_score = update_gap_two_vars(i - 1, j, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "above")
                above_value = value_matrix[i-1][j] - gap_score * need_constant_gap[i-1][j] + source_gap_score[i-1][j] * proportion - above_score[0] * proportion
                    
                value_matrix[i][j] = above_value
                source_matrix[i][j] = [i - 1,j]
                source_gap_score[i][j] = above_score[0]
                need_constant_gap[i][j] = 0
            elif i == 0:
                left_score = update_gap_two_vars(i, j - 1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "left")
                left_value = value_matrix[i][j-1] - gap_score * need_constant_gap[i][j-1] + source_gap_score[i][j-1] * proportion - left_score[0] * proportion
                    
                value_matrix[i][j] = left_value
                source_matrix[i][j] = [i,j-1]
                source_gap_score[i][j] = left_score[0]
                need_constant_gap[i][j] = 0
            else:
                score = align_score(X[i-1], Y[j-1])
                
                diag_score = update_gap_two_vars(i-1, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "diag")
                diag_value = value_matrix[i-1][j-1] + score + source_gap_score[i-1][j-1] * proportion- diag_score[0] * proportion
                    
                left_score = update_gap_two_vars(i, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "left")
                left_value = value_matrix[i][j-1] - gap_score * need_constant_gap[i][j-1] + source_gap_score[i][j-1] * proportion - left_score[0] * proportion
                
                above_score = update_gap_two_vars(i-1, j, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "above")
                above_value = value_matrix[i-1][j] - gap_score * need_constant_gap[i-1][j] + source_gap_score[i-1][j] * proportion - above_score[0] * proportion
                
                max_score = max(diag_value, left_value, above_value)
                value_matrix[i][j] = max_score
                if diag_value == max_score:
                    source_matrix[i][j] = [i -1, j-1]
                    source_gap_score[i][j] = 0
                    need_constant_gap[i][j] = 1
                elif left_value == max_score:
                    source_matrix[i][j] = [i,j-1]
                    if left_score[1] or above_score[1]:
                        source_gap_score[i][j] = 0
                        need_constant_gap[i][j] = 1
                    else:
                        source_gap_score[i][j] = left_score[0]
                        need_constant_gap[i][j] = 0
                else:
                    source_matrix[i][j] = [i -1,j]
                    if left_score[1] or above_score[1]:
                        source_gap_score[i][j] = 0
                        need_constant_gap[i][j] = 1
                    else:
                        source_gap_score[i][j] = above_score[0]
                        need_constant_gap[i][j] = 0
    # pretty_print(value_matrix)
    return value_matrix[len(X)][len(Y)]

def propogate_matrix_local_two_vars(X, Y, X1, Y1, X2, Y2, ratio, gap_score, align_score, proportion):
    X1.insert(0, 0)
    Y1.insert(0, 0)
    X2.insert(0, 0)
    Y2.insert(0, 0)
    
    value_matrix = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_matrix = [[[0, 0] for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    source_gap_score = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    need_constant_gap = [[0 for x in range(len(Y) + 1)] for x in range(len(X) + 1)]
    
    need_constant_gap[0][0] = 1
    
    for j in range(1, len(Y)+1):
        for i in range(1, len(X)+1):
            score = align_score(X[i-1], Y[j-1])

            diag_score = update_gap_two_vars(i-1, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "diag")
            diag_value = value_matrix[i-1][j-1] + score + source_gap_score[i-1][j-1] * proportion- diag_score[0] * proportion

            left_score = update_gap_two_vars(i, j-1, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "left")
            left_value = value_matrix[i][j-1] - gap_score * need_constant_gap[i][j-1] + source_gap_score[i][j-1] * proportion - left_score[0] * proportion

            above_score = update_gap_two_vars(i-1, j, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, "above")
            above_value = value_matrix[i-1][j] - gap_score * need_constant_gap[i-1][j] + source_gap_score[i-1][j] * proportion - above_score[0] * proportion

            max_score = max(diag_value, left_value, above_value, 0)
            value_matrix[i][j] = max_score
            if diag_value == max_score or max_score == 0:
                source_matrix[i][j] = [i-1, j-1]
                source_gap_score[i][j] = 0
                need_constant_gap[i][j] = 1
            elif left_value == max_score:
                source_matrix[i][j] = [i,j-1]
                if left_score[1] or above_score[1]:
                    source_gap_score[i][j] = 0
                    need_constant_gap[i][j] = 1
                else:
                    source_gap_score[i][j] = left_score[0]
                    need_constant_gap[i][j] = 0
            else:
                source_matrix[i][j] = [i -1,j]
                if left_score[1] or above_score[1]:
                    source_gap_score[i][j] = 0
                    need_constant_gap[i][j] = 1
                else:
                    source_gap_score[i][j] = above_score[0]
                    need_constant_gap[i][j] = 0
    # pretty_print(value_matrix)
    return value_matrix[len(X)][len(Y)]

# ratio 0-1, X/Y1 * ratio + X/Y2 * (1-ratio)
def update_gap_two_vars(row_index, column_index, source_matrix, X1, Y1, X2, Y2, ratio, source_gap_score, direction):
    # This means we are dealing with a value alongside the edge.
    if row_index == 0 or column_index == 0:
        return [abs(sum(X1[0:row_index+1]) - sum(Y1[0:column_index+1])) * ratio + abs(sum(X2[0:row_index+1]) - sum(Y2[0:column_index+1])) * (1-ratio), 0]
    # This means this value came from our diagonal direction.
    elif source_matrix[row_index][column_index][0] < row_index and source_matrix[row_index][column_index][1] < column_index:
        if direction == "left":
            return [Y1[column_index] * ratio + Y2[column_index] * (1-ratio), 0]
        elif direction == "above":
            return [X1[row_index] * ratio + X2[row_index] * (1-ratio), 0]
        else:
            return [abs(X1[row_index] - Y1[column_index]) * ratio + abs(X2[row_index] - Y2[column_index]) * (1-ratio), 0]
    # In this case, this value came from a downward movement, meaning an extended gap in the y-direction.
    elif source_matrix[row_index][column_index][0] < row_index:
        # This means that our best choice is a 'zigzag' movement.  So, we need to have the algorithm
        # reset the gap score, since we are now going to deal with a gap in the other sequence.
        if direction == "left":
            return [abs(source_gap_score[row_index][column_index] - Y1[column_index] * ratio - Y2[column_index] * (1-ratio)), 1]
        elif direction == "above":
            return [source_gap_score[row_index][column_index] + X1[row_index] * ratio + X2[row_index] * (1-ratio), 0]
        else:
            return [abs(source_gap_score[row_index][column_index] + (X1[row_index] - Y1[column_index]) * ratio + (X2[row_index] - Y2[column_index]) * (1-ratio)), 0]
    # In this case, this value came from a rightward movement, meaning an extended gap in the x-direction.
    elif source_matrix[row_index][column_index][1] < column_index:
        if direction == "left":
            return [source_gap_score[row_index][column_index] + Y1[column_index] * ratio + Y2[column_index] * (1-ratio), 0]
        # This means that our best choice is a 'zigzag' movement.  So, we need to have the algorithm
        # reset the gap score, since we are now going to deal with a gap in the other sequence.
        elif direction == "above":
            return [abs(source_gap_score[row_index][column_index] - X1[row_index] * ratio - X2[row_index] * (1-ratio)), 1]
        else:
            return [abs(source_gap_score[row_index][column_index] + (Y1[column_index ] - X1[row_index])*ratio + (Y2[column_index] - X2[row_index]) * (1-ratio)), 0]