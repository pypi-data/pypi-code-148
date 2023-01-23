# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import akeyless
from akeyless.models.gateway_migrate_personal_items import GatewayMigratePersonalItems  # noqa: E501
from akeyless.rest import ApiException

class TestGatewayMigratePersonalItems(unittest.TestCase):
    """GatewayMigratePersonalItems unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GatewayMigratePersonalItems
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.gateway_migrate_personal_items.GatewayMigratePersonalItems()  # noqa: E501
        if include_optional :
            return GatewayMigratePersonalItems(
                _1password_email = '0', 
                _1password_password = '0', 
                _1password_secret_key = '0', 
                _1password_url = '0', 
                _1password_vaults = [
                    '0'
                    ], 
                json = True, 
                protection_key = '0', 
                target_location = '0', 
                token = '0', 
                type = '1password', 
                uid_token = '0'
            )
        else :
            return GatewayMigratePersonalItems(
        )

    def testGatewayMigratePersonalItems(self):
        """Test GatewayMigratePersonalItems"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
