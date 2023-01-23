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


class UpdateGithubTarget(object):
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
        'comment': 'str',
        'github_app_id': 'int',
        'github_app_private_key': 'str',
        'github_base_url': 'str',
        'json': 'bool',
        'keep_prev_version': 'str',
        'key': 'str',
        'name': 'str',
        'new_name': 'str',
        'token': 'str',
        'uid_token': 'str',
        'update_version': 'bool'
    }

    attribute_map = {
        'comment': 'comment',
        'github_app_id': 'github-app-id',
        'github_app_private_key': 'github-app-private-key',
        'github_base_url': 'github-base-url',
        'json': 'json',
        'keep_prev_version': 'keep-prev-version',
        'key': 'key',
        'name': 'name',
        'new_name': 'new-name',
        'token': 'token',
        'uid_token': 'uid-token',
        'update_version': 'update-version'
    }

    def __init__(self, comment=None, github_app_id=None, github_app_private_key=None, github_base_url=None, json=None, keep_prev_version=None, key=None, name=None, new_name=None, token=None, uid_token=None, update_version=None, local_vars_configuration=None):  # noqa: E501
        """UpdateGithubTarget - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._comment = None
        self._github_app_id = None
        self._github_app_private_key = None
        self._github_base_url = None
        self._json = None
        self._keep_prev_version = None
        self._key = None
        self._name = None
        self._new_name = None
        self._token = None
        self._uid_token = None
        self._update_version = None
        self.discriminator = None

        if comment is not None:
            self.comment = comment
        if github_app_id is not None:
            self.github_app_id = github_app_id
        if github_app_private_key is not None:
            self.github_app_private_key = github_app_private_key
        if github_base_url is not None:
            self.github_base_url = github_base_url
        if json is not None:
            self.json = json
        if keep_prev_version is not None:
            self.keep_prev_version = keep_prev_version
        if key is not None:
            self.key = key
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if update_version is not None:
            self.update_version = update_version

    @property
    def comment(self):
        """Gets the comment of this UpdateGithubTarget.  # noqa: E501

        Comment about the target  # noqa: E501

        :return: The comment of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this UpdateGithubTarget.

        Comment about the target  # noqa: E501

        :param comment: The comment of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def github_app_id(self):
        """Gets the github_app_id of this UpdateGithubTarget.  # noqa: E501

        Github app id  # noqa: E501

        :return: The github_app_id of this UpdateGithubTarget.  # noqa: E501
        :rtype: int
        """
        return self._github_app_id

    @github_app_id.setter
    def github_app_id(self, github_app_id):
        """Sets the github_app_id of this UpdateGithubTarget.

        Github app id  # noqa: E501

        :param github_app_id: The github_app_id of this UpdateGithubTarget.  # noqa: E501
        :type: int
        """

        self._github_app_id = github_app_id

    @property
    def github_app_private_key(self):
        """Gets the github_app_private_key of this UpdateGithubTarget.  # noqa: E501

        App private key  # noqa: E501

        :return: The github_app_private_key of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._github_app_private_key

    @github_app_private_key.setter
    def github_app_private_key(self, github_app_private_key):
        """Sets the github_app_private_key of this UpdateGithubTarget.

        App private key  # noqa: E501

        :param github_app_private_key: The github_app_private_key of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._github_app_private_key = github_app_private_key

    @property
    def github_base_url(self):
        """Gets the github_base_url of this UpdateGithubTarget.  # noqa: E501

        Base URL  # noqa: E501

        :return: The github_base_url of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._github_base_url

    @github_base_url.setter
    def github_base_url(self, github_base_url):
        """Sets the github_base_url of this UpdateGithubTarget.

        Base URL  # noqa: E501

        :param github_base_url: The github_base_url of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._github_base_url = github_base_url

    @property
    def json(self):
        """Gets the json of this UpdateGithubTarget.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this UpdateGithubTarget.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this UpdateGithubTarget.

        Set output format to JSON  # noqa: E501

        :param json: The json of this UpdateGithubTarget.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def keep_prev_version(self):
        """Gets the keep_prev_version of this UpdateGithubTarget.  # noqa: E501


        :return: The keep_prev_version of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._keep_prev_version

    @keep_prev_version.setter
    def keep_prev_version(self, keep_prev_version):
        """Sets the keep_prev_version of this UpdateGithubTarget.


        :param keep_prev_version: The keep_prev_version of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._keep_prev_version = keep_prev_version

    @property
    def key(self):
        """Gets the key of this UpdateGithubTarget.  # noqa: E501

        The name of a key that used to encrypt the target secret value (if empty, the account default protectionKey key will be used)  # noqa: E501

        :return: The key of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this UpdateGithubTarget.

        The name of a key that used to encrypt the target secret value (if empty, the account default protectionKey key will be used)  # noqa: E501

        :param key: The key of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def name(self):
        """Gets the name of this UpdateGithubTarget.  # noqa: E501

        Target name  # noqa: E501

        :return: The name of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateGithubTarget.

        Target name  # noqa: E501

        :param name: The name of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this UpdateGithubTarget.  # noqa: E501

        New target name  # noqa: E501

        :return: The new_name of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this UpdateGithubTarget.

        New target name  # noqa: E501

        :param new_name: The new_name of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def token(self):
        """Gets the token of this UpdateGithubTarget.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdateGithubTarget.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdateGithubTarget.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdateGithubTarget.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdateGithubTarget.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdateGithubTarget.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def update_version(self):
        """Gets the update_version of this UpdateGithubTarget.  # noqa: E501

        Deprecated  # noqa: E501

        :return: The update_version of this UpdateGithubTarget.  # noqa: E501
        :rtype: bool
        """
        return self._update_version

    @update_version.setter
    def update_version(self, update_version):
        """Sets the update_version of this UpdateGithubTarget.

        Deprecated  # noqa: E501

        :param update_version: The update_version of this UpdateGithubTarget.  # noqa: E501
        :type: bool
        """

        self._update_version = update_version

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
        if not isinstance(other, UpdateGithubTarget):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateGithubTarget):
            return True

        return self.to_dict() != other.to_dict()
