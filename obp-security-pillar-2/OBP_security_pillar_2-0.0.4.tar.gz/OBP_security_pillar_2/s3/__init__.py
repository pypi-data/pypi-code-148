import logging

from OBP_security_pillar_2.s3.s3_bucket_logging_enabled import s3_bucket_logging_enabled
from OBP_security_pillar_2.s3.s3_bucket_versioning_enabled import s3_bucket_versioning_enabled
from OBP_security_pillar_2.s3.s3_bucket_public_read_prohibited import s3_bucket_public_read_prohibited
from OBP_security_pillar_2.s3.s3_bucket_public_write_prohibited import s3_bucket_public_write_prohibited
from OBP_security_pillar_2.s3.s3_bucket_server_side_encryption_enabled import s3_bucket_server_side_encryption_enabled
from OBP_security_pillar_2.s3.s3_default_encryption_kms import s3_default_encryption_kms
from OBP_security_pillar_2.s3.s3_bucket_ssl_requests_only import s3_bucket_ssl_requests_only

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def s3_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: s3_compliance()")

    response = [
        s3_bucket_versioning_enabled(self),
        s3_bucket_logging_enabled(self),
        s3_bucket_public_read_prohibited(self),
        s3_bucket_public_write_prohibited(self),
        s3_bucket_server_side_encryption_enabled(self),
        s3_default_encryption_kms(self),
        s3_bucket_ssl_requests_only(self)
    ]

    return response
