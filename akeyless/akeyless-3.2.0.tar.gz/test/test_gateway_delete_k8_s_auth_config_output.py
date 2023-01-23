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
from akeyless.models.gateway_delete_k8_s_auth_config_output import GatewayDeleteK8SAuthConfigOutput  # noqa: E501
from akeyless.rest import ApiException

class TestGatewayDeleteK8SAuthConfigOutput(unittest.TestCase):
    """GatewayDeleteK8SAuthConfigOutput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GatewayDeleteK8SAuthConfigOutput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.gateway_delete_k8_s_auth_config_output.GatewayDeleteK8SAuthConfigOutput()  # noqa: E501
        if include_optional :
            return GatewayDeleteK8SAuthConfigOutput(
                cluster_id = '0', 
                parts_change = akeyless.models.config_change.ConfigChange(
                    config_hash = akeyless.models.config_hash.ConfigHash(
                        admins = '0', 
                        cache = '0', 
                        customer_fragements = '0', 
                        general = '0', 
                        k8s_auths = '0', 
                        kmip = '0', 
                        ldap = '0', 
                        leadership = '0', 
                        log_forwarding = '0', 
                        migrations = '0', 
                        producers = akeyless.models.producers.producers(), 
                        rotators = akeyless.models.rotators.rotators(), 
                        saml = '0', 
                        universal_identity = '0', ), 
                    last_change = akeyless.models.last_config_change.LastConfigChange(
                        last_k8s_auths_change = akeyless.models.k8_s_auths_config_last_change.K8SAuthsConfigLastChange(
                            changed_k8s_auths_ids = [
                                '0'
                                ], 
                            created_k8s_auths_ids = [
                                '0'
                                ], 
                            deleted_k8s_auths_ids = [
                                '0'
                                ], ), 
                        last_migrations_change = akeyless.models.migrations_config_last_change.MigrationsConfigLastChange(
                            changed_migrations = [
                                '0'
                                ], 
                            created_migrations = [
                                '0'
                                ], 
                            deleted_migrations = [
                                '0'
                                ], ), ), 
                    last_status = akeyless.models.last_status_info.LastStatusInfo(
                        migrations_status = akeyless.models.migration_status.MigrationStatus(
                            last_messages = {
                                'key' : '0'
                                }, 
                            last_statuses = {
                                'key' : '0'
                                }, ), 
                        producers_errors = akeyless.models.producers_errors.producers_errors(), ), 
                    required_activity = akeyless.models.required_activity.RequiredActivity(
                        migrations_required_activity = {
                            'key' : True
                            }, ), 
                    update_stamp = 56, ), 
                total_hash = '0'
            )
        else :
            return GatewayDeleteK8SAuthConfigOutput(
        )

    def testGatewayDeleteK8SAuthConfigOutput(self):
        """Test GatewayDeleteK8SAuthConfigOutput"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
