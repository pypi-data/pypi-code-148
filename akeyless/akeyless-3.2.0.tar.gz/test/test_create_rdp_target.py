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
from akeyless.models.create_rdp_target import CreateRdpTarget  # noqa: E501
from akeyless.rest import ApiException

class TestCreateRdpTarget(unittest.TestCase):
    """CreateRdpTarget unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CreateRdpTarget
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.create_rdp_target.CreateRdpTarget()  # noqa: E501
        if include_optional :
            return CreateRdpTarget(
                admin_name = '0', 
                admin_pwd = '0', 
                comment = '0', 
                host_name = '0', 
                host_port = '0', 
                name = '0', 
                protection_key = '0', 
                token = '0', 
                uid_token = '0'
            )
        else :
            return CreateRdpTarget(
                name = '0',
        )

    def testCreateRdpTarget(self):
        """Test CreateRdpTarget"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
