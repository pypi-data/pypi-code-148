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


class GatewayUpdateProducerDockerhub(object):
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
        'delete_protection': 'str',
        'dockerhub_password': 'str',
        'dockerhub_token_scopes': 'str',
        'dockerhub_username': 'str',
        'json': 'bool',
        'name': 'str',
        'new_name': 'str',
        'producer_encryption_key_name': 'str',
        'tags': 'list[str]',
        'target_name': 'str',
        'token': 'str',
        'uid_token': 'str',
        'user_ttl': 'str'
    }

    attribute_map = {
        'delete_protection': 'delete_protection',
        'dockerhub_password': 'dockerhub-password',
        'dockerhub_token_scopes': 'dockerhub-token-scopes',
        'dockerhub_username': 'dockerhub-username',
        'json': 'json',
        'name': 'name',
        'new_name': 'new-name',
        'producer_encryption_key_name': 'producer-encryption-key-name',
        'tags': 'tags',
        'target_name': 'target-name',
        'token': 'token',
        'uid_token': 'uid-token',
        'user_ttl': 'user-ttl'
    }

    def __init__(self, delete_protection=None, dockerhub_password=None, dockerhub_token_scopes=None, dockerhub_username=None, json=None, name=None, new_name=None, producer_encryption_key_name=None, tags=None, target_name=None, token=None, uid_token=None, user_ttl='60m', local_vars_configuration=None):  # noqa: E501
        """GatewayUpdateProducerDockerhub - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._delete_protection = None
        self._dockerhub_password = None
        self._dockerhub_token_scopes = None
        self._dockerhub_username = None
        self._json = None
        self._name = None
        self._new_name = None
        self._producer_encryption_key_name = None
        self._tags = None
        self._target_name = None
        self._token = None
        self._uid_token = None
        self._user_ttl = None
        self.discriminator = None

        if delete_protection is not None:
            self.delete_protection = delete_protection
        if dockerhub_password is not None:
            self.dockerhub_password = dockerhub_password
        if dockerhub_token_scopes is not None:
            self.dockerhub_token_scopes = dockerhub_token_scopes
        if dockerhub_username is not None:
            self.dockerhub_username = dockerhub_username
        if json is not None:
            self.json = json
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if producer_encryption_key_name is not None:
            self.producer_encryption_key_name = producer_encryption_key_name
        if tags is not None:
            self.tags = tags
        if target_name is not None:
            self.target_name = target_name
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if user_ttl is not None:
            self.user_ttl = user_ttl

    @property
    def delete_protection(self):
        """Gets the delete_protection of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Protection from accidental deletion of this item  # noqa: E501

        :return: The delete_protection of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._delete_protection

    @delete_protection.setter
    def delete_protection(self, delete_protection):
        """Sets the delete_protection of this GatewayUpdateProducerDockerhub.

        Protection from accidental deletion of this item  # noqa: E501

        :param delete_protection: The delete_protection of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._delete_protection = delete_protection

    @property
    def dockerhub_password(self):
        """Gets the dockerhub_password of this GatewayUpdateProducerDockerhub.  # noqa: E501

        DockerhubPassword is either the user's password access token to manage the repository  # noqa: E501

        :return: The dockerhub_password of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._dockerhub_password

    @dockerhub_password.setter
    def dockerhub_password(self, dockerhub_password):
        """Sets the dockerhub_password of this GatewayUpdateProducerDockerhub.

        DockerhubPassword is either the user's password access token to manage the repository  # noqa: E501

        :param dockerhub_password: The dockerhub_password of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._dockerhub_password = dockerhub_password

    @property
    def dockerhub_token_scopes(self):
        """Gets the dockerhub_token_scopes of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Access token scopes list (comma-separated) to give the dynamic secret valid options are in \"repo:admin\", \"repo:write\", \"repo:read\", \"repo:public_read\"  # noqa: E501

        :return: The dockerhub_token_scopes of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._dockerhub_token_scopes

    @dockerhub_token_scopes.setter
    def dockerhub_token_scopes(self, dockerhub_token_scopes):
        """Sets the dockerhub_token_scopes of this GatewayUpdateProducerDockerhub.

        Access token scopes list (comma-separated) to give the dynamic secret valid options are in \"repo:admin\", \"repo:write\", \"repo:read\", \"repo:public_read\"  # noqa: E501

        :param dockerhub_token_scopes: The dockerhub_token_scopes of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._dockerhub_token_scopes = dockerhub_token_scopes

    @property
    def dockerhub_username(self):
        """Gets the dockerhub_username of this GatewayUpdateProducerDockerhub.  # noqa: E501

        DockerhubUsername is the name of the user in dockerhub  # noqa: E501

        :return: The dockerhub_username of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._dockerhub_username

    @dockerhub_username.setter
    def dockerhub_username(self, dockerhub_username):
        """Sets the dockerhub_username of this GatewayUpdateProducerDockerhub.

        DockerhubUsername is the name of the user in dockerhub  # noqa: E501

        :param dockerhub_username: The dockerhub_username of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._dockerhub_username = dockerhub_username

    @property
    def json(self):
        """Gets the json of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this GatewayUpdateProducerDockerhub.

        Set output format to JSON  # noqa: E501

        :param json: The json of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def name(self):
        """Gets the name of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Producer name  # noqa: E501

        :return: The name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewayUpdateProducerDockerhub.

        Producer name  # noqa: E501

        :param name: The name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Producer name  # noqa: E501

        :return: The new_name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this GatewayUpdateProducerDockerhub.

        Producer name  # noqa: E501

        :param new_name: The new_name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def producer_encryption_key_name(self):
        """Gets the producer_encryption_key_name of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Dynamic producer encryption key  # noqa: E501

        :return: The producer_encryption_key_name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._producer_encryption_key_name

    @producer_encryption_key_name.setter
    def producer_encryption_key_name(self, producer_encryption_key_name):
        """Sets the producer_encryption_key_name of this GatewayUpdateProducerDockerhub.

        Dynamic producer encryption key  # noqa: E501

        :param producer_encryption_key_name: The producer_encryption_key_name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._producer_encryption_key_name = producer_encryption_key_name

    @property
    def tags(self):
        """Gets the tags of this GatewayUpdateProducerDockerhub.  # noqa: E501

        List of the tags attached to this secret  # noqa: E501

        :return: The tags of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this GatewayUpdateProducerDockerhub.

        List of the tags attached to this secret  # noqa: E501

        :param tags: The tags of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def target_name(self):
        """Gets the target_name of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Target name  # noqa: E501

        :return: The target_name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this GatewayUpdateProducerDockerhub.

        Target name  # noqa: E501

        :param target_name: The target_name of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def token(self):
        """Gets the token of this GatewayUpdateProducerDockerhub.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayUpdateProducerDockerhub.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayUpdateProducerDockerhub.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayUpdateProducerDockerhub.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def user_ttl(self):
        """Gets the user_ttl of this GatewayUpdateProducerDockerhub.  # noqa: E501

        User TTL  # noqa: E501

        :return: The user_ttl of this GatewayUpdateProducerDockerhub.  # noqa: E501
        :rtype: str
        """
        return self._user_ttl

    @user_ttl.setter
    def user_ttl(self, user_ttl):
        """Sets the user_ttl of this GatewayUpdateProducerDockerhub.

        User TTL  # noqa: E501

        :param user_ttl: The user_ttl of this GatewayUpdateProducerDockerhub.  # noqa: E501
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
        if not isinstance(other, GatewayUpdateProducerDockerhub):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayUpdateProducerDockerhub):
            return True

        return self.to_dict() != other.to_dict()
