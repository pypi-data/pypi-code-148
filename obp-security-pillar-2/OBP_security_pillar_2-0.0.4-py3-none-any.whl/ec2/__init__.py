import logging

from OBP_security_pillar_2.ec2.ebs_snapshot_public_restorable_check import ebs_snapshot_public_restorable_check
from OBP_security_pillar_2.ec2.ec2_ebs_encryption_by_default import ec2_ebs_encryption_by_default
from OBP_security_pillar_2.ec2.ec2_imdsv2_check import ec2_imdsv2_check
from OBP_security_pillar_2.ec2.ec2_instance_managed_by_ssm import ec2_instance_managed_by_ssm
from OBP_security_pillar_2.ec2.ec2_instance_multiple_eni_check import ec2_instance_multiple_eni_check
from OBP_security_pillar_2.ec2.ec2_instance_profile_attached import ec2_instance_profile_attached
from OBP_security_pillar_2.ec2.ec2_volume_inuse_check import ec2_volume_inuse_check
from OBP_security_pillar_2.ec2.instance_in_vpc import instance_in_vpc
from OBP_security_pillar_2.ec2.ec2_encrypted_volume import ec2_encrypted_volume
from OBP_security_pillar_2.ec2.Incoming_ssh_disabled import incoming_ssh_disabled
from OBP_security_pillar_2.ec2.vpc_flow_logs_enabled import vpc_logging_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ec2_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_compliance()")

    response = [
        ec2_ebs_encryption_by_default(self),
        ec2_imdsv2_check(self),
        ec2_instance_managed_by_ssm(self),
        ec2_instance_multiple_eni_check(self),
        ec2_instance_profile_attached(self),
        ec2_volume_inuse_check(self),
        ebs_snapshot_public_restorable_check(self),
        # instance_in_vpc(self),
        # ec2_encrypted_volume(self),
        incoming_ssh_disabled(self),
        vpc_logging_enabled(self)
    ]

    return response
