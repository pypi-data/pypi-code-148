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
from iqs_client.models.repository_node_parent import RepositoryNodeParent  # noqa: E501
from iqs_client.rest import ApiException

class TestRepositoryNodeParent(unittest.TestCase):
    """RepositoryNodeParent unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RepositoryNodeParent
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = iqs_client.models.repository_node_parent.RepositoryNodeParent()  # noqa: E501
        if include_optional :
            return RepositoryNodeParent(
                id = [
                    '0'
                    ], 
                name = '0', 
                path = [
                    iqs_client.models.path_segment.PathSegment(
                        id_segment = '0', 
                        name = '0', )
                    ], 
                group_name = '0', 
                node_type = 'inode', 
                candidate_uri = '0', 
                children = []
            )
        else :
            return RepositoryNodeParent(
                id = [
                    '0'
                    ],
                name = '0',
                path = [
                    iqs_client.models.path_segment.PathSegment(
                        id_segment = '0', 
                        name = '0', )
                    ],
                group_name = '0',
                node_type = 'inode',
        )

    def testRepositoryNodeParent(self):
        """Test RepositoryNodeParent"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
