import logging
from OBP_reliability_pillar_4.elastic_load_balancer.cross_zone_load_balancing_enabled import \
    cross_zone_load_balancing_enabled
from OBP_reliability_pillar_4.elastic_load_balancer.elb_deletion_protection import elb_deletion_protection_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def elb_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_load_balancer :: elb_compliance()")

    response = [
        cross_zone_load_balancing_enabled(self),
        elb_deletion_protection_enabled(self)
    ]

    return response
