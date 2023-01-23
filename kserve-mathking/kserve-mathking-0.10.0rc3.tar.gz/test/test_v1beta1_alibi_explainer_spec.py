# Copyright 2021 The KServe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    KServe

    Python SDK for KServe  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import kserve
from kserve.models.v1beta1_alibi_explainer_spec import V1beta1AlibiExplainerSpec  # noqa: E501
from kserve.rest import ApiException

class TestV1beta1AlibiExplainerSpec(unittest.TestCase):
    """V1beta1AlibiExplainerSpec unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test V1beta1AlibiExplainerSpec
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kserve.models.v1beta1_alibi_explainer_spec.V1beta1AlibiExplainerSpec()  # noqa: E501
        if include_optional :
            return V1beta1AlibiExplainerSpec(
                args = [
                    '0'
                    ], 
                command = [
                    '0'
                    ], 
                config = {
                    'key' : '0'
                    }, 
                env = [
                    None
                    ], 
                env_from = [
                    None
                    ], 
                image = '0', 
                image_pull_policy = '0', 
                lifecycle = None, 
                liveness_probe = None, 
                name = '0', 
                ports = [
                    None
                    ], 
                readiness_probe = None, 
                resources = None, 
                runtime_version = '0', 
                security_context = None, 
                startup_probe = None, 
                stdin = True, 
                stdin_once = True, 
                storage_uri = '0', 
                termination_message_path = '0', 
                termination_message_policy = '0', 
                tty = True, 
                type = '0', 
                volume_devices = [
                    None
                    ], 
                volume_mounts = [
                    None
                    ], 
                working_dir = '0'
            )
        else :
            return V1beta1AlibiExplainerSpec(
                name = '0',
                type = '0',
        )

    def testV1beta1AlibiExplainerSpec(self):
        """Test V1beta1AlibiExplainerSpec"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
