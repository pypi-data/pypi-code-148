from boto3 import session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


__author__ = 'Dheeraj Banodha'
__version__ = '0.0.4'


class aws_client:
    def __init__(self, **kwargs):
        """
        @param str aws_access_key_id: AWS Access Key ID
        @param str aws_secret_access_key: AWS Secret Access Key
        """

        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

    from .rds import rds_compliance
    from .s3 import s3_compliance
    from .ec2 import ec2_compliance
    from .auto_scaling import auto_scaling_compliance
    from .cloudtrail import cloudtrail_compliance
    from .dynamodb import dynamodb_compliance
    from .guard_duty_enabled import guard_duty_enabled
    from .lambda_inside_vpc import lambda_inside_vpc
    # from .security_hub_enabled import security_hub_enabled
    from .elb_tls_https_listeners_only import elb_tls_https_listeners_only
    from .elb_logging_enabled import elb_logging_enabled

    # consolidate compliance.py details
    def get_compliance(self) -> list:
        """
        :return list: consolidated list  of compliance.py checks
        """
        logger.info(" ---Inside get_compliance()")

        compliance = [
            # self.security_hub_enabled(),
            self.elb_logging_enabled(),
            self.elb_tls_https_listeners_only(),
            # self.guard_duty_enabled(),
            # self.lambda_inside_vpc(),
        ]

        compliance.extend(self.rds_compliance())
        compliance.extend(self.s3_compliance())
        compliance.extend(self.ec2_compliance())
        compliance.extend(self.dynamodb_compliance())
        compliance.extend(self.auto_scaling_compliance())
        compliance.extend(self.cloudtrail_compliance())

        return compliance
