# Writing a pure Leiden function

def leiden_pure(Graph):
    optimiser = la.Optimiser()
    # Set initial partition
    partition = la.ModularityVertexPartition(Graph)
    refined_partition = la.ModularityVertexPartition(Graph)
    partition_agg = refined_partition.aggregate_partition()

    while optimiser.move_nodes(partition_agg):

        # Get individual membership for partition
        partition.from_coarse_partition(partition_agg, refined_partition.membership)

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