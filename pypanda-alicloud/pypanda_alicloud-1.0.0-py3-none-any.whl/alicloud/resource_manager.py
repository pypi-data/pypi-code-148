from typing import Iterator

from alibabacloud_resourcemanager20200331 import models as resource_manager_models
from alibabacloud_resourcemanager20200331.client import Client as ResourceManagerClient
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import tea_request_wrapper, page_reader


class ResourceManager(_Manager):
    def __init__(self, config: SessionConfig):
        super().__init__(config)
        self.config.endpoint = 'resourcemanager.aliyuncs.com'
        self.client = ResourceManagerClient(self.config)

    @page_reader(nodes=['resources', 'resource'])
    @tea_request_wrapper
    def iterate_all_resource(self, page_size=100, page_number=1) -> Iterator[resource_manager_models.ListResourcesResponseBodyResourcesResource]:
        list_resources_request = resource_manager_models.ListResourcesRequest(
            page_size=page_size,
            page_number=page_number
        )
        return self.client.list_resources_with_options(list_resources_request, self.runtimeOptions).body

    @page_reader(nodes=['accounts', 'account'])
    @tea_request_wrapper
    def iterate_accounts(self, page_size=100, page_number=1):
        get_folder_request = resource_manager_models.ListAccountsForParentRequest(
            page_size=page_size,
            page_number=page_number
        )
        return self.client.list_accounts_for_parent_with_options(get_folder_request, self.runtimeOptions).body
