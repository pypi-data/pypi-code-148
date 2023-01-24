"""
Contains the methods to check compliance for cloudwatch
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks the compliance for cloudwatch-log-group-encrypted
def log_group_encrypted(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside cloudwatch :: log_group_encrypted()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.18'
    compliance_type = 'Cloudwatch log group encrypted'
    description = 'Checks if a log group in Amazon CloudWatch Logs is encrypted with an AWS Key Management Service (' \
                  'KMS) key'
    resource_type = 'Cloudwatch logs'
    risk_level = 'Medium'

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

    # iterating through all the log groups
    for region, log_groups in kwargs['log_groups'].items():
        for log_group in log_groups:
            # Checking if log_group is encrypted with kms key or not
            try:
                key_id = log_group['kmsKeyId']
                if key_id == '':
                    result = False
                    offenders.append(log_group['logGroupName'])
                    failReason = 'Log group is not encrypted with KMS'
            except KeyError:
                result = False
                offenders.append(log_group['logGroupName'])
                failReason = 'Log group is not encrypted with KMS'

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


# compliance check for cloudwatch log group retention period
def log_group_retention_period_check(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside cloudwatch :: log_group_retention_period_check()--- ")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.22'
    compliance_type = 'Cloudwatch log group retention period check'
    description = 'Checks if Amazon CloudWatch LogGroup retention period is set to specific number of days (<=30)'
    resource_type = 'Cloudwatch logs'
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

    min_retention_time = 30

    # iterating through all the log groups
    for region, log_groups in kwargs['log_groups'].items():
        for log_group in log_groups:
            # checking the retention period of log group
            try:
                retention_period = log_group['retentionInDays']
                if retention_period > min_retention_time:
                    result = False
                    offenders.append(log_group['logGroupName'])
                    failReason = 'Log group has retention period set to either 0 or >30 days'
            except KeyError:
                result = False
                offenders.append(log_group['logGroupName'])
                failReason = 'Log group has retention period set to either 0 or >30 days'

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
