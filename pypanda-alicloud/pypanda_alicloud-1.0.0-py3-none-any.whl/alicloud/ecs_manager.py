from alibabacloud_ecs20140526 import models
from alibabacloud_ecs20140526.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class EcsManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.client = Client(self.config)

    @page_reader(nodes=['instances', 'instance'])
    def iterate_ecs(self, page_size=10, page_number=1, region_id="cn-shanghai", next_token=None):
        _r = models.DescribeInstancesRequest(region_id=region_id, page_size=page_size, page_number=page_number, next_token=next_token)
        return self.client.describe_instances_with_options(_r, self.runtimeOptions).body

    @page_reader(nodes=['security_groups', 'security_group'])
    @tea_request_wrapper
    def iterate_sg(self, page_size=30, page_number=1, region_id="cn-shanghai", next_token=None):
        _r = models.DescribeSecurityGroupsRequest(
            region_id=region_id, page_size=page_size, page_number=page_number
        )
        if next_token:
            _r.next_token = next_token
        return self.client.describe_security_groups_with_options(_r, self.runtimeOptions).body

    @tea_request_wrapper
    def get_sg_attr(self, sg_id, region_id=None):
        _r = models.DescribeSecurityGroupAttributeRequest(
            security_group_id=sg_id,
            region_id=region_id or self.region_id
        )
        return self.client.describe_security_group_attribute_with_options(_r, self.runtimeOptions).body
