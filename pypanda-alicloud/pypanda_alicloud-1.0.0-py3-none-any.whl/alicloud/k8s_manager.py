import Tea.exceptions
from alibabacloud_cs20151215.client import Client as K8sClient
from alibabacloud_cs20151215.models import *
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper
from .exceptions import ServiceNotEnabledError


class K8sManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.client = K8sClient(config)

    @page_reader(nodes=['clusters'])
    @tea_request_wrapper
    def iterate_k8s(self, page_size=10, page_number=1, region_id=None):
        _region = region_id or self.region_id
        _r = DescribeClustersV1Request(region_id=_region, page_size=page_size, page_number=page_number)
        try:
            res = self.client.describe_clusters_v1with_options(_r, {}, self.runtimeOptions)
            return res.body
        except Tea.exceptions.TeaException as e:
            import re
            regex = re.compile(r'The role not exists: acs:ram::\d+:role/aliyuncsdefaultrole')
            if regex.search(e.message):
                raise ServiceNotEnabledError("K8s service not enabled")
            raise e
