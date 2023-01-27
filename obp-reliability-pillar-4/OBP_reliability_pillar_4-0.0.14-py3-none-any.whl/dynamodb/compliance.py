import logging

from OBP_reliability_pillar_4.dynamodb.dynamodb_autoscaling_enabled import dynamodb_autoscaling_enabled
from OBP_reliability_pillar_4.dynamodb.dynamodb_pitr_enabled import dynamodb_pitr_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def dynamodb_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside dynamodb :: dynamodb_compliance()")

    response = [
        dynamodb_autoscaling_enabled(self),
        dynamodb_pitr_enabled(self),
    ]

    return response