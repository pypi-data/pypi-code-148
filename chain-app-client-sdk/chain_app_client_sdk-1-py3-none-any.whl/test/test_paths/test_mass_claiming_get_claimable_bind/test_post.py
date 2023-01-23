# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import chain_app_client_sdk
from chain_app_client_sdk.paths.mass_claiming_get_claimable_bind import post  # noqa: E501
from chain_app_client_sdk import configuration, schemas, api_client

from .. import ApiTestMixin


class TestMassClaimingGetClaimableBind(ApiTestMixin, unittest.TestCase):
    """
    MassClaimingGetClaimableBind unit test stubs
        getting claimable bind  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = post.ApiForpost(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 200




if __name__ == '__main__':
    unittest.main()
