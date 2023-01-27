import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks the compliance for the ec2 instance managed by systems manager
def ec2_instance_managed_by_ssm(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_instance_managed_by_ssm()")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.31'

    compliance_type = "EC2 instance managed by ssm"
    description = "Checks whether the Amazon EC2 instances in your account are managed by AWS Systems Manager"
    resource_type = "EC2"
    risk_level = 'High'

    regions = self.session.get_available_regions('ec2')

    for region in regions:
        try:
            client_ec2 = self.session.client('ec2', region_name=region)
            client_ssm = self.session.client('ssm', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response_ec2 = client_ec2.describe_instances()
                else:
                    response_ec2 = client_ec2.describe_instances(
                        NextToken=marker
                    )

                for reservation in response_ec2['Reservations']:
                    for instance in reservation['Instances']:
                        marker_ssm = ''
                        while True:
                            if marker == '':
                                response_ssm = client_ssm.describe_instance_information(
                                    InstanceInformationFilterList=[
                                        {
                                            'key': 'InstanceIds',
                                            'valueSet': [
                                                instance['InstanceId']
                                            ]
                                        }
                                    ]
                                )
                            else:
                                response_ssm = client_ssm.describe_instance_information(
                                    InstanceInformationFilterList=[
                                        {
                                            'key': 'InstanceIds',
                                            'valueSet': [
                                                instance['InstanceId']
                                            ]
                                        }
                                    ],
                                    NextToken=marker_ssm
                                )
                            if len(response_ssm['InstanceInformationList']) == 0:
                                failReason = "Instance is not managed by ssm"
                                result = False
                                offenders.append(instance['InstanceId'])

                            try:
                                marker = response_ssm['NextToken']
                                if marker == '':
                                    break
                            except KeyError:
                                break

                try:
                    marker = response_ec2['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            logging.warning("Something went wrong with the region {}: {}".format(region, e))

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
