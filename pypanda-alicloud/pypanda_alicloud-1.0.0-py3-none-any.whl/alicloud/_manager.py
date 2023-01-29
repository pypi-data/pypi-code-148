from alibabacloud_tea_openapi.models import Config as SessionConfig
from alibabacloud_tea_util import models as util_models


class _Manager:
    def __init__(self, config: SessionConfig):
        self.config = config
        self.runtimeOptions = util_models.RuntimeOptions(
            read_timeout=3000,
            max_attempts=3
        )
        self.region_id = 'cn-shanghai'

    @classmethod
    def from_assume_role_response(cls, data: dict, region="cn-shanghai"):
        credentials = data['Credentials']
        _conf = SessionConfig(
            access_key_id=credentials['AccessKeyId'],
            access_key_secret=credentials['AccessKeySecret'],
            security_token=credentials['SecurityToken'],
            type="StsToken",
            region_id=region
        )
        return cls(_conf)
