
def louvain_pure(Graph):
    optimiser = la.Optimiser()
    partition = la.ModularityVertexPartition(Graph)
    partition_agg = partition.aggregate_partition()
    while optimiser.move_nodes(partition_agg) > 0:
        partition.from_coarse_partition(partition_agg)
        partition_agg = partition_agg.aggregate_partition()   