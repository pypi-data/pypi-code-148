from alibabacloud_sts20150401 import models
from alibabacloud_sts20150401.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import tea_request_wrapper


class StsManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        config.endpoint = 'sts.cn-hangzhou.aliyuncs.com'
        self.client = Client(self.config)

    @tea_request_wrapper
    def assume_role(self, role_arn, role_session_name) -> models.AssumeRoleResponseBody:
        _r = models.AssumeRoleRequest(
            role_arn=role_arn,
            role_session_name=role_session_name
        )
        return self.client.assume_role_with_options(_r, self.runtimeOptions).body
