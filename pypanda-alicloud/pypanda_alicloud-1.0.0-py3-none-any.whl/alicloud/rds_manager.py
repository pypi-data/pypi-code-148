from alibabacloud_rds20140815 import models
from alibabacloud_rds20140815.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class RdsManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.client = Client(self.config)

    @page_reader(nodes=['items', 'dbinstance'])
    @tea_request_wrapper
    def iterate_rds(self, page_size=10, page_number=1, region_id="cn-shanghai"):
        _r = models.DescribeDBInstancesRequest(region_id=region_id, page_size=page_size,
                                               page_number=page_number)
        return self.client.describe_dbinstances_with_options(_r, self.runtimeOptions).body
