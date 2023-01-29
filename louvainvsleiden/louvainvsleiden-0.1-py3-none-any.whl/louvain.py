
import igraph as ig
import leidenalg as la


def louvain_test():
    print("I am the sexy Louvain test function")

# A function which puts all louvain partitions into one list

def louvain(Graph):

    # Initialise Optimiser class from Leidenalg
    optimiser = la.Optimiser()
    # Initialise empty list, which will store the partitions generated after each pass
    all_partitions_to_have_existed = []
    # 
    partition = la.ModularityVertexPartition(Graph)
    all_partitions_to_have_existed.append(copy.deepcopy(partition))

    partition_agg = partition.aggregate_partition()
    
    while optimiser.move_nodes(partition_agg) > 0:
        partition.from_coarse_partition(partition_agg)
        partition_agg = partition_agg.aggregate_partition()
        all_partitions_to_have_existed.append(copy.deepcopy(partition))

    return all_partitions_to_have_existed 