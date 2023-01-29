import federatedsecure.server


def create(accumulator_name):

    if accumulator_name == 'MinimumMaximum':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_basic_minimum_maximum import AccumulatorBasicMinimumMaximum
        return AccumulatorBasicMinimumMaximum

    if accumulator_name == 'SecureSum':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_basic_sum import AccumulatorSecureSum
        return AccumulatorSecureSum

    if accumulator_name == 'SecureMatrixMultiplication':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_generic import AccumulatorGeneric
        return AccumulatorGeneric

    if accumulator_name == 'SetIntersection':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_set_intersection import AccumulatorSetIntersection
        return AccumulatorSetIntersection

    if accumulator_name == 'SetIntersectionSize':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_set_intersection_size import AccumulatorSetIntersectionSize
        return AccumulatorSetIntersectionSize

    if accumulator_name == 'StatisticsBivariate':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_statistics_bivariate import AccumulatorStatisticsBivariate
        return AccumulatorStatisticsBivariate

    if accumulator_name == 'StatisticsFrequency':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_statistics_frequency import AccumulatorStatisticsFrequency
        return AccumulatorStatisticsFrequency

    if accumulator_name == 'StatisticsContingency':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_statistics_contingency import AccumulatorStatisticsContingency
        return AccumulatorStatisticsContingency

    if accumulator_name == 'StatisticsUnivariate':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_statistics_univariate import AccumulatorStatisticsUnivariate
        return AccumulatorStatisticsUnivariate

    if accumulator_name == 'StatisticsContingencyVertical':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_generic_dictionary import AccumulatorGenericDictionary
        return AccumulatorGenericDictionary

    if accumulator_name == 'StatisticsRegressionOLSVertical':
        from federatedsecure.server.plugins.simon.accumulators.accumulator_generic import AccumulatorGeneric
        return AccumulatorGeneric

    raise federatedsecure.server.server.exceptions.NotAvailable(accumulator_name)
