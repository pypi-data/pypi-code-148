import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks the compliance for the ec2_instance_multiple_eni_check
def ec2_instance_multiple_eni_check(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_instance_multiple_eni_check()")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id18.1'

    compliance_type = "Ec2 Instance multiple eni check"
    description = "Checks if Amazon Elastic Compute Cloud (Amazon EC2) uses multiple ENIs (Elastic Network Interfaces)"
    resource_type = "EC2"
    risk_level = 'Medium'

    regions = self.session.get_available_regions('ec2')

    for region in regions:
        try:
            client = self.session.client('ec2', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response = client.describe_instances()
                else:
                    response = client.describe_instances(
                        NextToken=marker
                    )
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:
                        if len(instance['NetworkInterfaces']) > 1:
                            result = False
                            failReason = 'Amazon Instance use multiple network interfaces'
                            offenders.append(instance['InstanceId'])

                try:
                    marker = response['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            logger.warning("Something went wrong with the region {}: {}".format(region, e))

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
