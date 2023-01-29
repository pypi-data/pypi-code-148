from alibabacloud_slb20140515 import models
from alibabacloud_slb20140515.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class SlbManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.client = Client(self.config)

    @page_reader(nodes=['load_balancers', 'load_balancer'])
    @tea_request_wrapper
    def iterate_slb(self, page_size=10, page_number=1, region_id="cn-shanghai"):
        _r = models.DescribeLoadBalancersRequest(region_id=region_id, page_size=page_size,
                                                 page_number=page_number)
        return self.client.describe_load_balancers_with_options(_r, self.runtimeOptions).body
