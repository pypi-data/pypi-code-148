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
from iqs_client.models.revision_details import RevisionDetails  # noqa: E501
from iqs_client.rest import ApiException

class TestRevisionDetails(unittest.TestCase):
    """RevisionDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RevisionDetails
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = iqs_client.models.revision_details.RevisionDetails()  # noqa: E501
        if include_optional :
            return RevisionDetails(
                workspace_title = 'Uncategorized', 
                resource_title = 'ICS-ALLQueries.MASTER', 
                branch_title = 'trunk', 
                compartment_label = '14', 
                author = 'Alice', 
                connector_name = 'Teamwork Cloud', 
                full_path = 'Teamwork Cloud / Uncategorized / ICS-ALLQueries.MASTER / trunk / 14', 
                container_path = 'Teamwork Cloud / Uncategorized / ICS-ALLQueries.MASTER / trunk'
            )
        else :
            return RevisionDetails(
                workspace_title = 'Uncategorized',
                resource_title = 'ICS-ALLQueries.MASTER',
                branch_title = 'trunk',
                compartment_label = '14',
                author = 'Alice',
                connector_name = 'Teamwork Cloud',
                full_path = 'Teamwork Cloud / Uncategorized / ICS-ALLQueries.MASTER / trunk / 14',
                container_path = 'Teamwork Cloud / Uncategorized / ICS-ALLQueries.MASTER / trunk',
        )

    def testRevisionDetails(self):
        """Test RevisionDetails"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
