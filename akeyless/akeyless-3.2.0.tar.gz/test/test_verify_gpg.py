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
from akeyless.models.verify_gpg import VerifyGPG  # noqa: E501
from akeyless.rest import ApiException

class TestVerifyGPG(unittest.TestCase):
    """VerifyGPG unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test VerifyGPG
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.verify_gpg.VerifyGPG()  # noqa: E501
        if include_optional :
            return VerifyGPG(
                display_id = '0', 
                item_id = 56, 
                json = True, 
                key_name = '0', 
                passphrase = '0', 
                signature = '0', 
                token = '0', 
                uid_token = '0'
            )
        else :
            return VerifyGPG(
                key_name = '0',
                signature = '0',
        )

    def testVerifyGPG(self):
        """Test VerifyGPG"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
