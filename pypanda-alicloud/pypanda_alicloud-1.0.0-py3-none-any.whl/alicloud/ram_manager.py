import json

from alibabacloud_ram20150501 import models
from alibabacloud_ram20150501.client import Client
from alibabacloud_tea_openapi.models import Config as SessionConfig

from ._manager import _Manager
from .decorator import page_reader, tea_request_wrapper


class RamManager(_Manager):
    def __init__(self, config: SessionConfig):
        config.endpoint = f'ram.aliyuncs.com'
        super().__init__(config)
        self.client = Client(self.config)

    @page_reader(nodes=['users', 'user'])
    @tea_request_wrapper
    def iterate_ram_user(self, page_size=50, marker=None):
        _r = models.ListUsersRequest(max_items=page_size, marker=marker)
        return self.client.list_users_with_options(_r, self.runtimeOptions).body

    @tea_request_wrapper
    def get_role(self, role_name):
        _r = models.GetRoleRequest(role_name=role_name)
        return self.client.get_role_with_options(_r, self.runtimeOptions).body
    @tea_request_wrapper
    def create_role(self, name, assume_role_policy_document, description=None):
        create_role_request = models.CreateRoleRequest(
            role_name=name,
            assume_role_policy_document=json.dumps(assume_role_policy_document))
        if description:
            create_role_request.description = description
        return self.client.create_role_with_options(create_role_request, self.runtimeOptions).body

    @tea_request_wrapper
    def attach_policy_to_role(self, policy_name, policy_type, role_name):
        attach_policy_to_role_request = models.AttachPolicyToRoleRequest(
            policy_name=policy_name,
            policy_type=policy_type,
            role_name=role_name
        )
        return self.client.attach_policy_to_role_with_options(attach_policy_to_role_request, self.runtimeOptions).body

    @tea_request_wrapper
    def create_policy(self,policy_name,policy_document):
        create_policy_request = models.CreatePolicyRequest(
            policy_name=policy_name,
            policy_document=json.dumps(policy_document)
        )
        return self.client.create_policy_with_options(create_policy_request, self.runtimeOptions).body

    @tea_request_wrapper
    def get_policy_document(self, policy_name, policy_type):
        """
        :param policy_name:
        :param policy_type: System or Custom
        :return:
        """
        get_policy_request = models.GetPolicyRequest(policy_name=policy_name, policy_type=policy_type)
        return self.client.get_policy_with_options(get_policy_request, self.runtimeOptions).body
