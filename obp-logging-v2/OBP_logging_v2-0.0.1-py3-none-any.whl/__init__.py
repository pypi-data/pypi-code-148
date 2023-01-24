from boto3 import session
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


__author__ = 'Klera DevOps'
__version__ = '0.0.1'


class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

    from .utils import get_regions, list_log_groups
    from .cloudwatch import log_group_encrypted, log_group_retention_period_check

    def get_compliance(self) -> list:
        """
        :return:
        """
        regions = self.get_regions()

        compliance = []

        try:
            log_groups = self.list_log_groups(regions=regions)
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.log_group_encrypted(exception=True, exception_text=e.response['Error']['Code'])),
            compliance.append(self.log_group_retention_period_check(exception=True, exception_text=e.response['Error']['Code']))
        else:
            compliance.append(self.log_group_encrypted(log_groups=log_groups)),
            compliance.append(self.log_group_retention_period_check(log_groups=log_groups))

        return compliance
