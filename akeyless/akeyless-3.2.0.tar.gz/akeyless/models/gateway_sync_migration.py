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


class GatewaySyncMigration(object):
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
        'json': 'bool',
        'name': 'str',
        'start_sync': 'bool',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'json': 'json',
        'name': 'name',
        'start_sync': 'start-sync',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, json=None, name=None, start_sync=None, token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """GatewaySyncMigration - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._json = None
        self._name = None
        self._start_sync = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        if json is not None:
            self.json = json
        self.name = name
        if start_sync is not None:
            self.start_sync = start_sync
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def json(self):
        """Gets the json of this GatewaySyncMigration.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this GatewaySyncMigration.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this GatewaySyncMigration.

        Set output format to JSON  # noqa: E501

        :param json: The json of this GatewaySyncMigration.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def name(self):
        """Gets the name of this GatewaySyncMigration.  # noqa: E501

        Migration name  # noqa: E501

        :return: The name of this GatewaySyncMigration.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewaySyncMigration.

        Migration name  # noqa: E501

        :param name: The name of this GatewaySyncMigration.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def start_sync(self):
        """Gets the start_sync of this GatewaySyncMigration.  # noqa: E501

        true, for starting synchronization, false for stopping  # noqa: E501

        :return: The start_sync of this GatewaySyncMigration.  # noqa: E501
        :rtype: bool
        """
        return self._start_sync

    @start_sync.setter
    def start_sync(self, start_sync):
        """Sets the start_sync of this GatewaySyncMigration.

        true, for starting synchronization, false for stopping  # noqa: E501

        :param start_sync: The start_sync of this GatewaySyncMigration.  # noqa: E501
        :type: bool
        """

        self._start_sync = start_sync

    @property
    def token(self):
        """Gets the token of this GatewaySyncMigration.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewaySyncMigration.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewaySyncMigration.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewaySyncMigration.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewaySyncMigration.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewaySyncMigration.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewaySyncMigration.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewaySyncMigration.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

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
        if not isinstance(other, GatewaySyncMigration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewaySyncMigration):
            return True

        return self.to_dict() != other.to_dict()
