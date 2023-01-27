import logging
from OBP_reliability_pillar_4.redshift.redshift_backup_enabled import redshift_backup_enabled
from OBP_reliability_pillar_4.redshift.redshift_cluster_maintenancesettings_check import \
    redshift_cluster_maintenance_settings_check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def  redshift_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside redshift :: redshift_compliance()")

    response = [
        redshift_backup_enabled(self),
        redshift_cluster_maintenance_settings_check(self),
    ]

    return response