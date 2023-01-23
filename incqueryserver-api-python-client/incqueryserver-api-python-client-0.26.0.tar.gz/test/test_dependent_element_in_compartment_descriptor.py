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
from iqs_client.models.dependent_element_in_compartment_descriptor import DependentElementInCompartmentDescriptor  # noqa: E501
from iqs_client.rest import ApiException

class TestDependentElementInCompartmentDescriptor(unittest.TestCase):
    """DependentElementInCompartmentDescriptor unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DependentElementInCompartmentDescriptor
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = iqs_client.models.dependent_element_in_compartment_descriptor.DependentElementInCompartmentDescriptor()  # noqa: E501
        if include_optional :
            return DependentElementInCompartmentDescriptor(
                reference = iqs_client.models.feature_descriptor_proxy.FeatureDescriptorProxy(
                    feature_name = '0', 
                    feature_kind = 'EATTRIBUTE', 
                    classifier_proxy = iqs_client.models.e_classifier_descriptor.EClassifierDescriptor(
                        classifier_name = '0', 
                        package_ns_uri = '0', ), ), 
                elements = [
                    iqs_client.models.dependent_element_details.DependentElementDetails(
                        name = 'Dependency1', 
                        element_id = '85827022-a8b5-4e6e-b604-9b7417cc7713', 
                        element_link = 'https://127.0.0.1:8111/osmc/workspaces/2394f5d1-1321-4f34-a373-cc1b159c7ebd/resources/34cc77c8-d3ef-40a6-9b91-65786117fe67/branches/bd03a239-7836-4d4c-9bcb-eba73b001b1e/revisions/1/elements/85827022-a8b5-4e6e-b604-9b7417cc7713', )
                    ]
            )
        else :
            return DependentElementInCompartmentDescriptor(
                reference = iqs_client.models.feature_descriptor_proxy.FeatureDescriptorProxy(
                    feature_name = '0', 
                    feature_kind = 'EATTRIBUTE', 
                    classifier_proxy = iqs_client.models.e_classifier_descriptor.EClassifierDescriptor(
                        classifier_name = '0', 
                        package_ns_uri = '0', ), ),
                elements = [
                    iqs_client.models.dependent_element_details.DependentElementDetails(
                        name = 'Dependency1', 
                        element_id = '85827022-a8b5-4e6e-b604-9b7417cc7713', 
                        element_link = 'https://127.0.0.1:8111/osmc/workspaces/2394f5d1-1321-4f34-a373-cc1b159c7ebd/resources/34cc77c8-d3ef-40a6-9b91-65786117fe67/branches/bd03a239-7836-4d4c-9bcb-eba73b001b1e/revisions/1/elements/85827022-a8b5-4e6e-b604-9b7417cc7713', )
                    ],
        )

    def testDependentElementInCompartmentDescriptor(self):
        """Test DependentElementInCompartmentDescriptor"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
