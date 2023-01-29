from alibabacloud_dds20151201.client import Client
from alibabacloud_dds20151201.models import *
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class MongoManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.config.endpoint = "mongodb.aliyuncs.com"
        self.client = Client(config)

    @page_reader(nodes=['dbinstances', 'dbinstance'])
    @tea_request_wrapper
    def iterate_mongodb(self, page_size=30, page_number=None, region_id="cn-shanghai"):
        _r = DescribeDBInstancesRequest(
            page_size=page_size,
            page_number=page_number,
            region_id=region_id
        )
        return self.client.describe_dbinstances_with_options(_r, self.runtimeOptions).body
