# Writing a function which calculates the Modularity of each partition in a list

def calc_mod_list(partition):
    mod_list = []
    for i in range(len(partition)):
        mod = partition[i].quality()
        mod_list.append(copy.deepcopy(mod))
    return mod_list

# Note: Extension idea: add other quality functions, e.g. betweenness centrality 