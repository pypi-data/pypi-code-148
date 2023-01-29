from alibabacloud_tea_openapi.models import Config as SessionConfig
from alibabacloud_vpc20160428.client import Client as VpcClient
from alibabacloud_vpc20160428.models import DescribeVpcsRequest, DescribeVpcsResponseBody, DescribeVSwitchesRequest, \
    DescribeVSwitchesResponseBody

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class VpcManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.client = VpcClient(self.config)

    @page_reader(nodes=['vpcs', 'vpc'])
    @tea_request_wrapper
    def iterate_vpc(self, page_size=10, page_number=1, region_id="cn-shanghai") -> DescribeVpcsResponseBody:
        _r = DescribeVpcsRequest(region_id=region_id, page_size=page_size, page_number=page_number)
        return self.client.describe_vpcs_with_options(_r, self.runtimeOptions).body

    @page_reader(nodes=['v_switches', 'v_switch'])
    @tea_request_wrapper
    def iterate_vsw(self, page_size=10, page_number=1, region_id="cn-shanghai") -> DescribeVSwitchesResponseBody:
        _r = DescribeVSwitchesRequest(
            region_id=region_id,
            page_size=page_size,
            page_number=page_number
        )
        return self.client.describe_vswitches_with_options(_r, self.runtimeOptions).body
