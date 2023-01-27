from .rds_automatic_minor_version_upgrade_enabled import *
from .rds_instance_public_access_check import *
from .rds_snapshot_encrypted import rds_snapshot_encrypted
from .rds_snapshots_public_prohibited import rds_snapshots_public_prohibited
from .rds_storage_encrypted import rds_storage_encrypted


def rds_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside rds :: rds_compliance()")

    response = [
        # rds_automatic_minor_version_upgrade_enabled(self),
        rds_instance_public_access_check(self),
        rds_snapshot_encrypted(self),
        rds_snapshots_public_prohibited(self),
        rds_storage_encrypted(self),
    ]

    return response
