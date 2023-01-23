# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from akeyless.configuration import Configuration


class GatewayCreateProducerAzure(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'app_obj_id': 'str',
        'azure_client_id': 'str',
        'azure_client_secret': 'str',
        'azure_tenant_id': 'str',
        'delete_protection': 'str',
        'fixed_user_claim_keyname': 'str',
        'fixed_user_only': 'bool',
        'json': 'bool',
        'name': 'str',
        'producer_encryption_key_name': 'str',
        'secure_access_enable': 'str',
        'secure_access_web': 'bool',
        'secure_access_web_browsing': 'bool',
        'secure_access_web_proxy': 'bool',
        'tags': 'list[str]',
        'target_name': 'str',
        'token': 'str',
        'uid_token': 'str',
        'user_group_obj_id': 'str',
        'user_portal_access': 'bool',
        'user_principal_name': 'str',
        'user_programmatic_access': 'bool',
        'user_role_template_id': 'str',
        'user_ttl': 'str'
    }

    attribute_map = {
        'app_obj_id': 'app-obj-id',
        'azure_client_id': 'azure-client-id',
        'azure_client_secret': 'azure-client-secret',
        'azure_tenant_id': 'azure-tenant-id',
        'delete_protection': 'delete_protection',
        'fixed_user_claim_keyname': 'fixed-user-claim-keyname',
        'fixed_user_only': 'fixed-user-only',
        'json': 'json',
        'name': 'name',
        'producer_encryption_key_name': 'producer-encryption-key-name',
        'secure_access_enable': 'secure-access-enable',
        'secure_access_web': 'secure-access-web',
        'secure_access_web_browsing': 'secure-access-web-browsing',
        'secure_access_web_proxy': 'secure-access-web-proxy',
        'tags': 'tags',
        'target_name': 'target-name',
        'token': 'token',
        'uid_token': 'uid-token',
        'user_group_obj_id': 'user-group-obj-id',
        'user_portal_access': 'user-portal-access',
        'user_principal_name': 'user-principal-name',
        'user_programmatic_access': 'user-programmatic-access',
        'user_role_template_id': 'user-role-template-id',
        'user_ttl': 'user-ttl'
    }

    def __init__(self, app_obj_id=None, azure_client_id=None, azure_client_secret=None, azure_tenant_id=None, delete_protection=None, fixed_user_claim_keyname='false', fixed_user_only=False, json=None, name=None, producer_encryption_key_name=None, secure_access_enable=None, secure_access_web=None, secure_access_web_browsing=None, secure_access_web_proxy=None, tags=None, target_name=None, token=None, uid_token=None, user_group_obj_id=None, user_portal_access=False, user_principal_name=None, user_programmatic_access=False, user_role_template_id=None, user_ttl='60m', local_vars_configuration=None):  # noqa: E501
        """GatewayCreateProducerAzure - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._app_obj_id = None
        self._azure_client_id = None
        self._azure_client_secret = None
        self._azure_tenant_id = None
        self._delete_protection = None
        self._fixed_user_claim_keyname = None
        self._fixed_user_only = None
        self._json = None
        self._name = None
        self._producer_encryption_key_name = None
        self._secure_access_enable = None
        self._secure_access_web = None
        self._secure_access_web_browsing = None
        self._secure_access_web_proxy = None
        self._tags = None
        self._target_name = None
        self._token = None
        self._uid_token = None
        self._user_group_obj_id = None
        self._user_portal_access = None
        self._user_principal_name = None
        self._user_programmatic_access = None
        self._user_role_template_id = None
        self._user_ttl = None
        self.discriminator = None

        if app_obj_id is not None:
            self.app_obj_id = app_obj_id
        if azure_client_id is not None:
            self.azure_client_id = azure_client_id
        if azure_client_secret is not None:
            self.azure_client_secret = azure_client_secret
        if azure_tenant_id is not None:
            self.azure_tenant_id = azure_tenant_id
        if delete_protection is not None:
            self.delete_protection = delete_protection
        if fixed_user_claim_keyname is not None:
            self.fixed_user_claim_keyname = fixed_user_claim_keyname
        if fixed_user_only is not None:
            self.fixed_user_only = fixed_user_only
        if json is not None:
            self.json = json
        self.name = name
        if producer_encryption_key_name is not None:
            self.producer_encryption_key_name = producer_encryption_key_name
        if secure_access_enable is not None:
            self.secure_access_enable = secure_access_enable
        if secure_access_web is not None:
            self.secure_access_web = secure_access_web
        if secure_access_web_browsing is not None:
            self.secure_access_web_browsing = secure_access_web_browsing
        if secure_access_web_proxy is not None:
            self.secure_access_web_proxy = secure_access_web_proxy
        if tags is not None:
            self.tags = tags
        if target_name is not None:
            self.target_name = target_name
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if user_group_obj_id is not None:
            self.user_group_obj_id = user_group_obj_id
        if user_portal_access is not None:
            self.user_portal_access = user_portal_access
        if user_principal_name is not None:
            self.user_principal_name = user_principal_name
        if user_programmatic_access is not None:
            self.user_programmatic_access = user_programmatic_access
        if user_role_template_id is not None:
            self.user_role_template_id = user_role_template_id
        if user_ttl is not None:
            self.user_ttl = user_ttl

    @property
    def app_obj_id(self):
        """Gets the app_obj_id of this GatewayCreateProducerAzure.  # noqa: E501

        Azure App Object Id  # noqa: E501

        :return: The app_obj_id of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._app_obj_id

    @app_obj_id.setter
    def app_obj_id(self, app_obj_id):
        """Sets the app_obj_id of this GatewayCreateProducerAzure.

        Azure App Object Id  # noqa: E501

        :param app_obj_id: The app_obj_id of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._app_obj_id = app_obj_id

    @property
    def azure_client_id(self):
        """Gets the azure_client_id of this GatewayCreateProducerAzure.  # noqa: E501

        Azure Client ID  # noqa: E501

        :return: The azure_client_id of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._azure_client_id

    @azure_client_id.setter
    def azure_client_id(self, azure_client_id):
        """Sets the azure_client_id of this GatewayCreateProducerAzure.

        Azure Client ID  # noqa: E501

        :param azure_client_id: The azure_client_id of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._azure_client_id = azure_client_id

    @property
    def azure_client_secret(self):
        """Gets the azure_client_secret of this GatewayCreateProducerAzure.  # noqa: E501

        Azure Client Secret  # noqa: E501

        :return: The azure_client_secret of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._azure_client_secret

    @azure_client_secret.setter
    def azure_client_secret(self, azure_client_secret):
        """Sets the azure_client_secret of this GatewayCreateProducerAzure.

        Azure Client Secret  # noqa: E501

        :param azure_client_secret: The azure_client_secret of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._azure_client_secret = azure_client_secret

    @property
    def azure_tenant_id(self):
        """Gets the azure_tenant_id of this GatewayCreateProducerAzure.  # noqa: E501

        Azure Tenant ID  # noqa: E501

        :return: The azure_tenant_id of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._azure_tenant_id

    @azure_tenant_id.setter
    def azure_tenant_id(self, azure_tenant_id):
        """Sets the azure_tenant_id of this GatewayCreateProducerAzure.

        Azure Tenant ID  # noqa: E501

        :param azure_tenant_id: The azure_tenant_id of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._azure_tenant_id = azure_tenant_id

    @property
    def delete_protection(self):
        """Gets the delete_protection of this GatewayCreateProducerAzure.  # noqa: E501

        Protection from accidental deletion of this item  # noqa: E501

        :return: The delete_protection of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._delete_protection

    @delete_protection.setter
    def delete_protection(self, delete_protection):
        """Sets the delete_protection of this GatewayCreateProducerAzure.

        Protection from accidental deletion of this item  # noqa: E501

        :param delete_protection: The delete_protection of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._delete_protection = delete_protection

    @property
    def fixed_user_claim_keyname(self):
        """Gets the fixed_user_claim_keyname of this GatewayCreateProducerAzure.  # noqa: E501

        FixedUserClaimKeyname  # noqa: E501

        :return: The fixed_user_claim_keyname of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._fixed_user_claim_keyname

    @fixed_user_claim_keyname.setter
    def fixed_user_claim_keyname(self, fixed_user_claim_keyname):
        """Sets the fixed_user_claim_keyname of this GatewayCreateProducerAzure.

        FixedUserClaimKeyname  # noqa: E501

        :param fixed_user_claim_keyname: The fixed_user_claim_keyname of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._fixed_user_claim_keyname = fixed_user_claim_keyname

    @property
    def fixed_user_only(self):
        """Gets the fixed_user_only of this GatewayCreateProducerAzure.  # noqa: E501

        Fixed user  # noqa: E501

        :return: The fixed_user_only of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._fixed_user_only

    @fixed_user_only.setter
    def fixed_user_only(self, fixed_user_only):
        """Sets the fixed_user_only of this GatewayCreateProducerAzure.

        Fixed user  # noqa: E501

        :param fixed_user_only: The fixed_user_only of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._fixed_user_only = fixed_user_only

    @property
    def json(self):
        """Gets the json of this GatewayCreateProducerAzure.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this GatewayCreateProducerAzure.

        Set output format to JSON  # noqa: E501

        :param json: The json of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def name(self):
        """Gets the name of this GatewayCreateProducerAzure.  # noqa: E501

        Producer name  # noqa: E501

        :return: The name of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewayCreateProducerAzure.

        Producer name  # noqa: E501

        :param name: The name of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def producer_encryption_key_name(self):
        """Gets the producer_encryption_key_name of this GatewayCreateProducerAzure.  # noqa: E501

        Dynamic producer encryption key  # noqa: E501

        :return: The producer_encryption_key_name of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._producer_encryption_key_name

    @producer_encryption_key_name.setter
    def producer_encryption_key_name(self, producer_encryption_key_name):
        """Sets the producer_encryption_key_name of this GatewayCreateProducerAzure.

        Dynamic producer encryption key  # noqa: E501

        :param producer_encryption_key_name: The producer_encryption_key_name of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._producer_encryption_key_name = producer_encryption_key_name

    @property
    def secure_access_enable(self):
        """Gets the secure_access_enable of this GatewayCreateProducerAzure.  # noqa: E501


        :return: The secure_access_enable of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._secure_access_enable

    @secure_access_enable.setter
    def secure_access_enable(self, secure_access_enable):
        """Sets the secure_access_enable of this GatewayCreateProducerAzure.


        :param secure_access_enable: The secure_access_enable of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._secure_access_enable = secure_access_enable

    @property
    def secure_access_web(self):
        """Gets the secure_access_web of this GatewayCreateProducerAzure.  # noqa: E501


        :return: The secure_access_web of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._secure_access_web

    @secure_access_web.setter
    def secure_access_web(self, secure_access_web):
        """Sets the secure_access_web of this GatewayCreateProducerAzure.


        :param secure_access_web: The secure_access_web of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._secure_access_web = secure_access_web

    @property
    def secure_access_web_browsing(self):
        """Gets the secure_access_web_browsing of this GatewayCreateProducerAzure.  # noqa: E501


        :return: The secure_access_web_browsing of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._secure_access_web_browsing

    @secure_access_web_browsing.setter
    def secure_access_web_browsing(self, secure_access_web_browsing):
        """Sets the secure_access_web_browsing of this GatewayCreateProducerAzure.


        :param secure_access_web_browsing: The secure_access_web_browsing of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._secure_access_web_browsing = secure_access_web_browsing

    @property
    def secure_access_web_proxy(self):
        """Gets the secure_access_web_proxy of this GatewayCreateProducerAzure.  # noqa: E501


        :return: The secure_access_web_proxy of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._secure_access_web_proxy

    @secure_access_web_proxy.setter
    def secure_access_web_proxy(self, secure_access_web_proxy):
        """Sets the secure_access_web_proxy of this GatewayCreateProducerAzure.


        :param secure_access_web_proxy: The secure_access_web_proxy of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._secure_access_web_proxy = secure_access_web_proxy

    @property
    def tags(self):
        """Gets the tags of this GatewayCreateProducerAzure.  # noqa: E501

        List of the tags attached to this secret  # noqa: E501

        :return: The tags of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this GatewayCreateProducerAzure.

        List of the tags attached to this secret  # noqa: E501

        :param tags: The tags of this GatewayCreateProducerAzure.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def target_name(self):
        """Gets the target_name of this GatewayCreateProducerAzure.  # noqa: E501

        Target name  # noqa: E501

        :return: The target_name of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this GatewayCreateProducerAzure.

        Target name  # noqa: E501

        :param target_name: The target_name of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def token(self):
        """Gets the token of this GatewayCreateProducerAzure.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayCreateProducerAzure.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayCreateProducerAzure.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayCreateProducerAzure.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def user_group_obj_id(self):
        """Gets the user_group_obj_id of this GatewayCreateProducerAzure.  # noqa: E501

        User Group Object Id  # noqa: E501

        :return: The user_group_obj_id of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._user_group_obj_id

    @user_group_obj_id.setter
    def user_group_obj_id(self, user_group_obj_id):
        """Sets the user_group_obj_id of this GatewayCreateProducerAzure.

        User Group Object Id  # noqa: E501

        :param user_group_obj_id: The user_group_obj_id of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._user_group_obj_id = user_group_obj_id

    @property
    def user_portal_access(self):
        """Gets the user_portal_access of this GatewayCreateProducerAzure.  # noqa: E501

        Azure User portal access  # noqa: E501

        :return: The user_portal_access of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._user_portal_access

    @user_portal_access.setter
    def user_portal_access(self, user_portal_access):
        """Sets the user_portal_access of this GatewayCreateProducerAzure.

        Azure User portal access  # noqa: E501

        :param user_portal_access: The user_portal_access of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._user_portal_access = user_portal_access

    @property
    def user_principal_name(self):
        """Gets the user_principal_name of this GatewayCreateProducerAzure.  # noqa: E501

        User Principal Name  # noqa: E501

        :return: The user_principal_name of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._user_principal_name

    @user_principal_name.setter
    def user_principal_name(self, user_principal_name):
        """Sets the user_principal_name of this GatewayCreateProducerAzure.

        User Principal Name  # noqa: E501

        :param user_principal_name: The user_principal_name of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._user_principal_name = user_principal_name

    @property
    def user_programmatic_access(self):
        """Gets the user_programmatic_access of this GatewayCreateProducerAzure.  # noqa: E501

        Azure User programmatic access  # noqa: E501

        :return: The user_programmatic_access of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: bool
        """
        return self._user_programmatic_access

    @user_programmatic_access.setter
    def user_programmatic_access(self, user_programmatic_access):
        """Sets the user_programmatic_access of this GatewayCreateProducerAzure.

        Azure User programmatic access  # noqa: E501

        :param user_programmatic_access: The user_programmatic_access of this GatewayCreateProducerAzure.  # noqa: E501
        :type: bool
        """

        self._user_programmatic_access = user_programmatic_access

    @property
    def user_role_template_id(self):
        """Gets the user_role_template_id of this GatewayCreateProducerAzure.  # noqa: E501

        User Role Template Id  # noqa: E501

        :return: The user_role_template_id of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._user_role_template_id

    @user_role_template_id.setter
    def user_role_template_id(self, user_role_template_id):
        """Sets the user_role_template_id of this GatewayCreateProducerAzure.

        User Role Template Id  # noqa: E501

        :param user_role_template_id: The user_role_template_id of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._user_role_template_id = user_role_template_id

    @property
    def user_ttl(self):
        """Gets the user_ttl of this GatewayCreateProducerAzure.  # noqa: E501

        User TTL  # noqa: E501

        :return: The user_ttl of this GatewayCreateProducerAzure.  # noqa: E501
        :rtype: str
        """
        return self._user_ttl

    @user_ttl.setter
    def user_ttl(self, user_ttl):
        """Sets the user_ttl of this GatewayCreateProducerAzure.

        User TTL  # noqa: E501

        :param user_ttl: The user_ttl of this GatewayCreateProducerAzure.  # noqa: E501
        :type: str
        """

        self._user_ttl = user_ttl

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GatewayCreateProducerAzure):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayCreateProducerAzure):
            return True

        return self.to_dict() != other.to_dict()
