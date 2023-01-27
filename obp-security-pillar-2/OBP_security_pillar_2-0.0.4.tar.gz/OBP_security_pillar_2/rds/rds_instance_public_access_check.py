import logging
import botocore
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def rds_instance_public_access_check(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside rds :: rds_instance_public_access_check()")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id1.10'

    compliance_type = "RDS instance public access check"
    description = "Checks whether the Amazon Relational Database Service (RDS) instances are not publicly accessible"
    resource_type = "RDS Instance"
    risk_level = 'High'

    regions = self.session.get_available_regions('rds')

    for region in regions:
        try:
            client = self.session.client('rds', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response = client.describe_db_instances()
                else:
                    response = client.describe_db_instances(
                        Marker=marker
                    )

                for instance in response['DBInstances']:
                    if instance['PubliclyAccessible']:
                        result = False
                        failReason = "RDS instance is publicly accessible"
                        offenders.append(instance['DBInstanceIdentifier'])

                try:
                    marker = response['Marker']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            logger.error("Something went wrong with the region {}: {}".format(region, e))

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
