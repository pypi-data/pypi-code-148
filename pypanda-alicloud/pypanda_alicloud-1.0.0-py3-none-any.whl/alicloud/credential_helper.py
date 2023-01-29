import json
import uuid

from alibabacloud_tea_openapi.models import Config

from pypanda.alicloud.exceptions import *
from pypanda.alicloud.ram_manager import RamManager
from pypanda.alicloud.sts_manager import StsManager


class IkeaAliCloudCredentialHelper:
    def __init__(self, config: Config):
        # Resource Directory account
        self.account_rd = "1174006592814680"
        # Account cannot not join Resource Directory.[Owned by 'IKEA e-commerce company'].Use role CMSAdmin to manage
        self.ecommerce_accounts = [
            "1971113059044309",
            "1445012382022038",
            "1492332401850327",
            "1160173615814831",
            "1224273617588681"
        ]
        self.ecommerce_accounts_admin_role = "CloudAdmin"
        self.default_accounts_admin_role = "ResourceDirectoryAccountAccessRole"
        self.config = config

    def get_admin_arn(self, account):
        if account in self.ecommerce_accounts:
            return f"acs:ram::{account}:role/{self.ecommerce_accounts_admin_role}"
        elif account == self.account_rd:
            return f"acs:ram::{account}:role/CloudAdmin"
        else:
            return f"acs:ram::{account}:role/{self.default_accounts_admin_role}"

    def get_admin_sts(self, account):
        """
        Get admin sts token for account. Required self.config has Full AssumeRole permission
        :param account:
        :return:
        """
        sts_client = StsManager(self.config)
        return sts_client.assume_role(
            role_arn=self.get_admin_arn(account),
            role_session_name=uuid.uuid4().hex
        ).to_map()

    def get_readonly_sts(self, account):
        """
        Get readonly sts token for account. Required self.config is CloudObserver Role of Resource Directory account
        :param account:
        :return:
        """
        sts_client = StsManager(self.config)
        return sts_client.assume_role(
            role_arn=f"acs:ram::{account}:role/CloudObserver",
            role_session_name=uuid.uuid4().hex
        ).to_map()


def ensure_cloud_observer_role(manager):
    manager = RamManager.from_assume_role_response(d)
    trust_role_policy = {
        "Statement": [
            {"Action": "sts:AssumeRole", "Effect": "Allow", "Principal": {"RAM": "acs:ram::1174006592814680:root"}}
        ],
        "Version": "1"
    }

    assume_role_policy = {
        "Version": "1",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": "acs:ram:*:*:role/CloudObserver"
            }
        ]
    }
    role_name = "CloudObserver"
    policy_name = "CloudObserverSTS"
    try:
        role = manager.get_role(role_name)
    except EntityNotExists as e:
        role = manager.create_role(role_name, trust_role_policy)
    try:
        policy = manager.get_policy_document(policy_name, 'Custom')
        assert json.loads(policy.default_policy_version.policy_document) == assume_role_policy
    except EntityNotExists:
        policy = manager.create_policy(policy_name, assume_role_policy)
    # try:
    #     manager.attach_policy_to_role(policy_name, 'Custom', role_name)
    # except EntityAlreadyExists:
    #     pass

    try:
        manager.attach_policy_to_role('ReadOnlyAccess', 'System', role_name)
    except EntityAlreadyExists:
        pass
