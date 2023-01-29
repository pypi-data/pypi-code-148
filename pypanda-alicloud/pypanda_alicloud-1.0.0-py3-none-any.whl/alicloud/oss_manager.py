from alibabacloud_oss20190517 import models
from alibabacloud_oss20190517.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class OssManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.client = Client(self.config)

    @page_reader(nodes=['buckets', 'buckets'])
    @tea_request_wrapper
    def iterate_oss(self, page_size=10, marker=None):
        _r = models.ListBucketsRequest(
            marker=marker,
            max_keys=page_size
        )
        _ = self.client.list_buckets_with_options(_r, {}, self.runtimeOptions)
        return _.body
