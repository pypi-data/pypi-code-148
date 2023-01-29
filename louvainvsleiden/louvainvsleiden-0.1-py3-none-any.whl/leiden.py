# A function which puts all leiden partitions into one list

def leiden(Graph):
    optimiser = la.Optimiser()
    all_partitions_to_have_existed = []

    # Set initial partition
    partition = la.ModularityVertexPartition(Graph)
    all_partitions_to_have_existed.append(copy.deepcopy(partition))
    refined_partition = la.ModularityVertexPartition(Graph)
    partition_agg = refined_partition.aggregate_partition()

    while optimiser.move_nodes(partition_agg):

        # Get individual membership for partition
        partition.from_coarse_partition(partition_agg, refined_partition.membership)
        all_partitions_to_have_existed.append(copy.deepcopy(partition))

        # Refine partition
        refined_partition = la.ModularityVertexPartition(Graph)
        optimiser.merge_nodes_constrained(refined_partition, partition)

        # Define aggregate partition on refined partition
        partition_agg = refined_partition.aggregate_partition()

        # But use membership of actual partition
        aggregate_membership = [None] * len(refined_partition)
        for i in range(Graph.vcount()):
            aggregate_membership[refined_partition.membership[i]] = partition.membership[i]
        
        partition_agg.set_membership(aggregate_membership)
        
    return all_partitions_to_have_existed
