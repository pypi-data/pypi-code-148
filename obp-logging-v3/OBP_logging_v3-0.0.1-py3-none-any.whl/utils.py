import logging

import botocore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_regions(self):
    logger.info(" ---Inside utils :: get_regions()--- ")
    """Summary

    Returns:
        TYPE: Description
    """

    client = self.session.client('ec2', region_name='us-east-1')
    region_response = {}
    try:
        region_response = client.describe_regions()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AuthFailure':
            logger.error(f" AccessKey credentails not found here: {error}")
            exit(1)
    except botocore.exceptions.NoCredentialsError as e:
        logger.error(f" Unable to locate credentials: {e} ")
        exit(1)

    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions


# returns the list of log groups
def list_log_groups(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_log_groups()--- ")

    log_groups = {}

    for region in regions:
        # Connect to the cloudwatch log service
        client = self.session.client('logs', region_name=region)
        marker = ''
        while True:
            # list all log groups
            if marker == '':
                response = client.describe_log_groups()
            else:
                response = client.describe_log_groups(
                    nextToken=marker
                )
            # adding the list of log groups to the log_groups
            log_groups.setdefault(region, []).extend(response['logGroups'])

            # trying to fetch the nextToken
            try:
                marker = response['nextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return log_groups


# returns the list of rds instances
def list_rds_instances(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_instances()--- ")
    rds_list = {}

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_instances()
            else:
                response = client.describe_db_instances(
                    Marker=marker
                )
            rds_list.setdefault(region, []).extend(response['DBInstances'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return rds_list
