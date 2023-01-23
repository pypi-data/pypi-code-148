# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: placeHolderApiVersion
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import iqs_client
from iqs_client.models.md_object_id_list import MDObjectIDList  # noqa: E501
from iqs_client.rest import ApiException

class TestMDObjectIDList(unittest.TestCase):
    """MDObjectIDList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MDObjectIDList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = iqs_client.models.md_object_id_list.MDObjectIDList()  # noqa: E501
        if include_optional :
            return MDObjectIDList(
                md_object_ids = [
                    '_10_0EAPbeta2_8740266_1126081779875_694366_861'
                    ], 
                include_only_latest_revisions_of_branches = True
            )
        else :
            return MDObjectIDList(
                md_object_ids = [
                    '_10_0EAPbeta2_8740266_1126081779875_694366_861'
                    ],
        )

    def testMDObjectIDList(self):
        """Test MDObjectIDList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
