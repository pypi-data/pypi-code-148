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


class GatewayGetLdapAuthConfigOutput(object):
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
        'ldap_access_id': 'str',
        'ldap_anonymous_search': 'bool',
        'ldap_bind_dn': 'str',
        'ldap_bind_password': 'str',
        'ldap_cert': 'str',
        'ldap_enable': 'bool',
        'ldap_group_attr': 'str',
        'ldap_group_dn': 'str',
        'ldap_group_filter': 'str',
        'ldap_private_key': 'str',
        'ldap_token_expiration': 'str',
        'ldap_url': 'str',
        'ldap_user_attr': 'str',
        'ldap_user_dn': 'str'
    }

    attribute_map = {
        'ldap_access_id': 'ldap_access_id',
        'ldap_anonymous_search': 'ldap_anonymous_search',
        'ldap_bind_dn': 'ldap_bind_dn',
        'ldap_bind_password': 'ldap_bind_password',
        'ldap_cert': 'ldap_cert',
        'ldap_enable': 'ldap_enable',
        'ldap_group_attr': 'ldap_group_attr',
        'ldap_group_dn': 'ldap_group_dn',
        'ldap_group_filter': 'ldap_group_filter',
        'ldap_private_key': 'ldap_private_key',
        'ldap_token_expiration': 'ldap_token_expiration',
        'ldap_url': 'ldap_url',
        'ldap_user_attr': 'ldap_user_attr',
        'ldap_user_dn': 'ldap_user_dn'
    }

    def __init__(self, ldap_access_id=None, ldap_anonymous_search=None, ldap_bind_dn=None, ldap_bind_password=None, ldap_cert=None, ldap_enable=None, ldap_group_attr=None, ldap_group_dn=None, ldap_group_filter=None, ldap_private_key=None, ldap_token_expiration=None, ldap_url=None, ldap_user_attr=None, ldap_user_dn=None, local_vars_configuration=None):  # noqa: E501
        """GatewayGetLdapAuthConfigOutput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._ldap_access_id = None
        self._ldap_anonymous_search = None
        self._ldap_bind_dn = None
        self._ldap_bind_password = None
        self._ldap_cert = None
        self._ldap_enable = None
        self._ldap_group_attr = None
        self._ldap_group_dn = None
        self._ldap_group_filter = None
        self._ldap_private_key = None
        self._ldap_token_expiration = None
        self._ldap_url = None
        self._ldap_user_attr = None
        self._ldap_user_dn = None
        self.discriminator = None

        if ldap_access_id is not None:
            self.ldap_access_id = ldap_access_id
        if ldap_anonymous_search is not None:
            self.ldap_anonymous_search = ldap_anonymous_search
        if ldap_bind_dn is not None:
            self.ldap_bind_dn = ldap_bind_dn
        if ldap_bind_password is not None:
            self.ldap_bind_password = ldap_bind_password
        if ldap_cert is not None:
            self.ldap_cert = ldap_cert
        if ldap_enable is not None:
            self.ldap_enable = ldap_enable
        if ldap_group_attr is not None:
            self.ldap_group_attr = ldap_group_attr
        if ldap_group_dn is not None:
            self.ldap_group_dn = ldap_group_dn
        if ldap_group_filter is not None:
            self.ldap_group_filter = ldap_group_filter
        if ldap_private_key is not None:
            self.ldap_private_key = ldap_private_key
        if ldap_token_expiration is not None:
            self.ldap_token_expiration = ldap_token_expiration
        if ldap_url is not None:
            self.ldap_url = ldap_url
        if ldap_user_attr is not None:
            self.ldap_user_attr = ldap_user_attr
        if ldap_user_dn is not None:
            self.ldap_user_dn = ldap_user_dn

    @property
    def ldap_access_id(self):
        """Gets the ldap_access_id of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_access_id of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_access_id

    @ldap_access_id.setter
    def ldap_access_id(self, ldap_access_id):
        """Sets the ldap_access_id of this GatewayGetLdapAuthConfigOutput.


        :param ldap_access_id: The ldap_access_id of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_access_id = ldap_access_id

    @property
    def ldap_anonymous_search(self):
        """Gets the ldap_anonymous_search of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_anonymous_search of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: bool
        """
        return self._ldap_anonymous_search

    @ldap_anonymous_search.setter
    def ldap_anonymous_search(self, ldap_anonymous_search):
        """Sets the ldap_anonymous_search of this GatewayGetLdapAuthConfigOutput.


        :param ldap_anonymous_search: The ldap_anonymous_search of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: bool
        """

        self._ldap_anonymous_search = ldap_anonymous_search

    @property
    def ldap_bind_dn(self):
        """Gets the ldap_bind_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_bind_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_bind_dn

    @ldap_bind_dn.setter
    def ldap_bind_dn(self, ldap_bind_dn):
        """Sets the ldap_bind_dn of this GatewayGetLdapAuthConfigOutput.


        :param ldap_bind_dn: The ldap_bind_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_bind_dn = ldap_bind_dn

    @property
    def ldap_bind_password(self):
        """Gets the ldap_bind_password of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_bind_password of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_bind_password

    @ldap_bind_password.setter
    def ldap_bind_password(self, ldap_bind_password):
        """Sets the ldap_bind_password of this GatewayGetLdapAuthConfigOutput.


        :param ldap_bind_password: The ldap_bind_password of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_bind_password = ldap_bind_password

    @property
    def ldap_cert(self):
        """Gets the ldap_cert of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_cert of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_cert

    @ldap_cert.setter
    def ldap_cert(self, ldap_cert):
        """Sets the ldap_cert of this GatewayGetLdapAuthConfigOutput.


        :param ldap_cert: The ldap_cert of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_cert = ldap_cert

    @property
    def ldap_enable(self):
        """Gets the ldap_enable of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_enable of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: bool
        """
        return self._ldap_enable

    @ldap_enable.setter
    def ldap_enable(self, ldap_enable):
        """Sets the ldap_enable of this GatewayGetLdapAuthConfigOutput.


        :param ldap_enable: The ldap_enable of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: bool
        """

        self._ldap_enable = ldap_enable

    @property
    def ldap_group_attr(self):
        """Gets the ldap_group_attr of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_group_attr of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_group_attr

    @ldap_group_attr.setter
    def ldap_group_attr(self, ldap_group_attr):
        """Sets the ldap_group_attr of this GatewayGetLdapAuthConfigOutput.


        :param ldap_group_attr: The ldap_group_attr of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_group_attr = ldap_group_attr

    @property
    def ldap_group_dn(self):
        """Gets the ldap_group_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_group_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_group_dn

    @ldap_group_dn.setter
    def ldap_group_dn(self, ldap_group_dn):
        """Sets the ldap_group_dn of this GatewayGetLdapAuthConfigOutput.


        :param ldap_group_dn: The ldap_group_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_group_dn = ldap_group_dn

    @property
    def ldap_group_filter(self):
        """Gets the ldap_group_filter of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_group_filter of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_group_filter

    @ldap_group_filter.setter
    def ldap_group_filter(self, ldap_group_filter):
        """Sets the ldap_group_filter of this GatewayGetLdapAuthConfigOutput.


        :param ldap_group_filter: The ldap_group_filter of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_group_filter = ldap_group_filter

    @property
    def ldap_private_key(self):
        """Gets the ldap_private_key of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_private_key of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_private_key

    @ldap_private_key.setter
    def ldap_private_key(self, ldap_private_key):
        """Sets the ldap_private_key of this GatewayGetLdapAuthConfigOutput.


        :param ldap_private_key: The ldap_private_key of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_private_key = ldap_private_key

    @property
    def ldap_token_expiration(self):
        """Gets the ldap_token_expiration of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_token_expiration of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_token_expiration

    @ldap_token_expiration.setter
    def ldap_token_expiration(self, ldap_token_expiration):
        """Sets the ldap_token_expiration of this GatewayGetLdapAuthConfigOutput.


        :param ldap_token_expiration: The ldap_token_expiration of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_token_expiration = ldap_token_expiration

    @property
    def ldap_url(self):
        """Gets the ldap_url of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_url of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_url

    @ldap_url.setter
    def ldap_url(self, ldap_url):
        """Sets the ldap_url of this GatewayGetLdapAuthConfigOutput.


        :param ldap_url: The ldap_url of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_url = ldap_url

    @property
    def ldap_user_attr(self):
        """Gets the ldap_user_attr of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_user_attr of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_user_attr

    @ldap_user_attr.setter
    def ldap_user_attr(self, ldap_user_attr):
        """Sets the ldap_user_attr of this GatewayGetLdapAuthConfigOutput.


        :param ldap_user_attr: The ldap_user_attr of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_user_attr = ldap_user_attr

    @property
    def ldap_user_dn(self):
        """Gets the ldap_user_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501


        :return: The ldap_user_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :rtype: str
        """
        return self._ldap_user_dn

    @ldap_user_dn.setter
    def ldap_user_dn(self, ldap_user_dn):
        """Sets the ldap_user_dn of this GatewayGetLdapAuthConfigOutput.


        :param ldap_user_dn: The ldap_user_dn of this GatewayGetLdapAuthConfigOutput.  # noqa: E501
        :type: str
        """

        self._ldap_user_dn = ldap_user_dn

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
        if not isinstance(other, GatewayGetLdapAuthConfigOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayGetLdapAuthConfigOutput):
            return True

        return self.to_dict() != other.to_dict()
