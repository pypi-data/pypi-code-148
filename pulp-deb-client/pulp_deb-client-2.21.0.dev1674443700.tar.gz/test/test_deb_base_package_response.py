# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_deb
from pulpcore.client.pulp_deb.models.deb_base_package_response import DebBasePackageResponse  # noqa: E501
from pulpcore.client.pulp_deb.rest import ApiException

class TestDebBasePackageResponse(unittest.TestCase):
    """DebBasePackageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DebBasePackageResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_deb.models.deb_base_package_response.DebBasePackageResponse()  # noqa: E501
        if include_optional :
            return DebBasePackageResponse(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                artifact = '0', 
                relative_path = '0', 
                md5 = '0', 
                sha1 = '0', 
                sha224 = '0', 
                sha256 = '0', 
                sha384 = '0', 
                sha512 = '0', 
                package = '0', 
                source = '0', 
                version = '0', 
                architecture = '0', 
                section = '0', 
                priority = '0', 
                origin = '0', 
                tag = '0', 
                bugs = '0', 
                essential = '0', 
                build_essential = '0', 
                installed_size = '0', 
                maintainer = '0', 
                original_maintainer = '0', 
                description = '0', 
                description_md5 = '0', 
                homepage = '0', 
                built_using = '0', 
                auto_built_package = '0', 
                multi_arch = '0', 
                breaks = '0', 
                conflicts = '0', 
                depends = '0', 
                recommends = '0', 
                suggests = '0', 
                enhances = '0', 
                pre_depends = '0', 
                provides = '0', 
                replaces = '0'
            )
        else :
            return DebBasePackageResponse(
        )

    def testDebBasePackageResponse(self):
        """Test DebBasePackageResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
