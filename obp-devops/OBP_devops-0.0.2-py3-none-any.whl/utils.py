import logging

import botocore
from botocore.exceptions import ClientError, EndpointConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns the list of regions
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


# returns the list of elastic beanstalk environments
def list_elastic_beanstalk_envs(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_elastic_beanstalk_envs()---")

    environments = {}

    for region in regions:
        try:
            client = self.session.client('elasticbeanstalk', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response_describe_eb = client.describe_environments()
                else:
                    response_describe_eb = client.describe_environments(
                        NextToken=marker
                    )
                for env in response_describe_eb['Environments']:
                    environments.setdefault(region, []).append(env)

                try:
                    marker = response_describe_eb['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break
        except ClientError as e:
            logger.error("Something went wrong with region {}: {}".format(region, e))

    return environments


# returns the list eks clusters
def list_eks_clusters(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_eks_clusters()--- ")

    clusters_lst = {}

    for region in regions:
        client = self.session.client('eks', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.list_clusters()
            else:
                response = client.list_clusters(
                    nextToken=marker
                )

            clusters_lst.setdefault(region, []).extend(response['clusters'])
            try:
                marker = response['nextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return clusters_lst


# returns the list of ecr repositories
def list_ecr_repositories(self, regions: list) -> dict:
    """
    :param self:
    :param region:
    :return:
    """
    logger.info(" ---Inside utils :: list_ecr_repositories()--- ")

    repos = {}

    for region in regions:
        client = self.session.client('ecr', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_repositories()
            else:
                response = client.describe_repositories(
                    nextToken=marker
                )
            repos.setdefault(region, []).extend(response['repositories'])

            try:
                marker = response['nextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return repos


# returns the list of codebuild projects
def list_codebuild_projects(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_codebuild_project()--- ")

    project_lst = {}

    for region in regions:
        client = self.session.client('codebuild', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.list_projects()
            else:
                response = client.list_projects(
                    nextToken=marker
                )
            project_lst.setdefault(region, []).extend(response['projects'])

            try:
                marker = response['nextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return project_lst


# returns the list of code pipelines
def list_code_pipelines(self, regions: list) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_code_pipelines()--- ")

    pipelines = {}

    for region in regions:
        try:
            client = self.session.client('codepipeline', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response = client.list_pipelines()
                else:
                    response = client.list_pipelines(
                        nextToken=marker
                    )
                pipelines.setdefault(region, []).extend(response['pipelines'])

                try:
                    marker = response['nextToken']
                    if marker == '':
                        break
                except KeyError:
                    break
        except EndpointConnectionError as e:
            pass

    return pipelines
