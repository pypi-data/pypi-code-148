import logging
import botocore
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance.py for rds automatic minor version enabled
def rds_storage_encrypted(self) -> dict:
    """
    :param self:
    :return dict:
    """
    logger.info(" ---Inside rds :: rds_storage_encrypted()")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id1.12'

    compliance_type = "RDS Storage Encrypted"
    description = "Checks whether storage encryption is enabled for your RDS DB instances"
    resource_type = "RDS"
    risk_level = 'High'

    regions = self.session.get_available_regions('rds')

    for region in regions:
        try:
            client = self.session.client('rds', region_name=region)
            marker = ''
            while True:
                response = client.describe_db_instances(
                    MaxRecords=100,
                    Marker=marker
                )
                for instance in response['DBInstances']:
                    storage_encryption = instance['StorageEncrypted']
                    if not storage_encryption:
                        result = False
                        failReason = "Storage encryption is not enabled"
                        offenders.append(region+': '+instance['DBInstanceIdentifier'])

                try:
                    marker = response['Marker']
                    if marker == '':
                        break
                except KeyError:
                    break
        except botocore.exceptions.ClientError as e:
            logger.error('Something went wrong with region {}: {}'.format(region, e))

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
