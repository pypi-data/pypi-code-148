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
from iqs_client.models.branch_with_dependent_elements import BranchWithDependentElements  # noqa: E501
from iqs_client.rest import ApiException

class TestBranchWithDependentElements(unittest.TestCase):
    """BranchWithDependentElements unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test BranchWithDependentElements
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = iqs_client.models.branch_with_dependent_elements.BranchWithDependentElements()  # noqa: E501
        if include_optional :
            return BranchWithDependentElements(
                branch_id = 'trunk', 
                title = '958bd4bb-a145-48bf-a1df-da10803b6233', 
                revisions = [
                    null
                    ]
            )
        else :
            return BranchWithDependentElements(
                branch_id = 'trunk',
                revisions = [
                    null
                    ],
        )

    def testBranchWithDependentElements(self):
        """Test BranchWithDependentElements"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
