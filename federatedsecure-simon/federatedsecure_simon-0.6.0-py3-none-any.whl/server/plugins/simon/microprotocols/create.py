import federatedsecure.server
import federatedsecure.server.server.exceptions


def create(microprotocol):

    if microprotocol == 'MinimumMaximum':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_minimum_maximum import MicroprotocolMinimumMaximum
        return MicroprotocolMinimumMaximum

    if microprotocol == 'SecureSum':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_secure_sum import MicroprotocolSecureSum
        return MicroprotocolSecureSum

    if microprotocol == 'SecureMatrixMultiplication':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_secure_matrix_multiplication import MicroprotocolSecureMatrixMultiplication
        return MicroprotocolSecureMatrixMultiplication

    if microprotocol == 'SetIntersection':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_set_intersection import MicroprotocolSetIntersection
        return MicroprotocolSetIntersection

    if microprotocol == 'SetIntersectionSize':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_set_intersection_size import MicroprotocolSetIntersectionSize
        return MicroprotocolSetIntersectionSize

    if microprotocol == 'StatisticsBivariate':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_statistics_bivariate import MicroprotocolStatisticsBivariate
        return MicroprotocolStatisticsBivariate

    if microprotocol == 'StatisticsFrequency':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_statistics_frequency import MicroprotocolStatisticsFrequency
        return MicroprotocolStatisticsFrequency

    if microprotocol == 'StatisticsContingency':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_statistics_contingency import MicroprotocolStatisticsContingency
        return MicroprotocolStatisticsContingency

    if microprotocol == 'StatisticsUnivariate':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_statistics_univariate import MicroprotocolStatisticsUnivariate
        return MicroprotocolStatisticsUnivariate

    if microprotocol == 'StatisticsContingencyVertical':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_statistics_contingency_vertical import MicroprotocolStatisticsContingencyVertical
        return MicroprotocolStatisticsContingencyVertical

    if microprotocol == 'StatisticsRegressionOLSVertical':
        from federatedsecure.server.plugins.simon.microprotocols.microprotocol_statistics_regression_ols_vertical import MicroprotocolStatisticsRegressionOLSVertical
        return MicroprotocolStatisticsRegressionOLSVertical

    raise federatedsecure.server.server.exceptions.NotAvailable(microprotocol)
