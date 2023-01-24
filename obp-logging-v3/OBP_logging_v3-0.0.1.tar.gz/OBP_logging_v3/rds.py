"""
Contains the methods to check compliance for rds
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance for rds logging enabled
def rds_logging_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :param rds_lst:
    :return:
    """
    logger.info(" ---Inside rds :: rds_logging_enabled()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.77'
    compliance_type = 'RDS Logging Enabled'
    description = 'Checks that respective logs of Amazon Relational Database Service (Amazon RDS) are enabled'
    resource_type = 'RDS'
    risk_level = 'Low'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, instances in kwargs['rds_lst'].items():
        for instance in instances:
            try:
                if len(instance['EnabledCloudwatchLogsExports']) <= 0:
                    result = False
                    failReason = "RDS logging is not enabled"
                    offenders.append(instance['DBInstanceIdentifier'])
            except KeyError:
                result = False
                failReason = "RDS logging is not enabled"
                offenders.append(instance['DBInstanceIdentifier'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }

