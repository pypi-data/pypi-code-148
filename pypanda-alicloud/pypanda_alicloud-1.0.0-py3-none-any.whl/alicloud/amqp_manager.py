from Tea.exceptions import TeaException
from alibabacloud_amqp_open20191212 import models
from alibabacloud_amqp_open20191212.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper
from .exceptions import ServiceNotEnabledError


class AmqpManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.config.endpoint = f'amqp-open.{self.region_id}.aliyuncs.com'
        self.client = Client(self.config)

    @page_reader(nodes=['data', 'instances'])
    @tea_request_wrapper
    def iterate_amqp(self, next_token=None, page_size=10):
        _r = models.ListInstancesRequest(next_token, max_results=page_size)
        try:
            return self.client.list_instances_with_options(_r, self.runtimeOptions).body
        except TeaException as e:
            if 'The request has failed due to unauthorized operation' in e.message:
                """Compatibility trick for aliCloud Api,since it will return UnAuthorized error when the service is not enabled"""
                raise ServiceNotEnabledError("AMQP Service is not enabled")
            raise e
