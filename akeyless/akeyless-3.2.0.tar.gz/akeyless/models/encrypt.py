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


class Encrypt(object):
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
        'display_id': 'str',
        'encryption_context': 'dict(str, str)',
        'input_format': 'str',
        'item_id': 'int',
        'json': 'bool',
        'key_name': 'str',
        'plaintext': 'str',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'display_id': 'display-id',
        'encryption_context': 'encryption-context',
        'input_format': 'input-format',
        'item_id': 'item-id',
        'json': 'json',
        'key_name': 'key-name',
        'plaintext': 'plaintext',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, display_id=None, encryption_context=None, input_format=None, item_id=None, json=None, key_name=None, plaintext=None, token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """Encrypt - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._display_id = None
        self._encryption_context = None
        self._input_format = None
        self._item_id = None
        self._json = None
        self._key_name = None
        self._plaintext = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        if display_id is not None:
            self.display_id = display_id
        if encryption_context is not None:
            self.encryption_context = encryption_context
        if input_format is not None:
            self.input_format = input_format
        if item_id is not None:
            self.item_id = item_id
        if json is not None:
            self.json = json
        self.key_name = key_name
        if plaintext is not None:
            self.plaintext = plaintext
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def display_id(self):
        """Gets the display_id of this Encrypt.  # noqa: E501

        The display id of the key to use in the encryption process  # noqa: E501

        :return: The display_id of this Encrypt.  # noqa: E501
        :rtype: str
        """
        return self._display_id

    @display_id.setter
    def display_id(self, display_id):
        """Sets the display_id of this Encrypt.

        The display id of the key to use in the encryption process  # noqa: E501

        :param display_id: The display_id of this Encrypt.  # noqa: E501
        :type: str
        """

        self._display_id = display_id

    @property
    def encryption_context(self):
        """Gets the encryption_context of this Encrypt.  # noqa: E501

        name-value pair that specifies the encryption context to be used for authenticated encryption. If used here, the same value must be supplied to the decrypt command or decryption will fail  # noqa: E501

        :return: The encryption_context of this Encrypt.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._encryption_context

    @encryption_context.setter
    def encryption_context(self, encryption_context):
        """Sets the encryption_context of this Encrypt.

        name-value pair that specifies the encryption context to be used for authenticated encryption. If used here, the same value must be supplied to the decrypt command or decryption will fail  # noqa: E501

        :param encryption_context: The encryption_context of this Encrypt.  # noqa: E501
        :type: dict(str, str)
        """

        self._encryption_context = encryption_context

    @property
    def input_format(self):
        """Gets the input_format of this Encrypt.  # noqa: E501

        If specified, the plaintext input is assumed to be formatted accordingly. Current supported options: [base64]  # noqa: E501

        :return: The input_format of this Encrypt.  # noqa: E501
        :rtype: str
        """
        return self._input_format

    @input_format.setter
    def input_format(self, input_format):
        """Sets the input_format of this Encrypt.

        If specified, the plaintext input is assumed to be formatted accordingly. Current supported options: [base64]  # noqa: E501

        :param input_format: The input_format of this Encrypt.  # noqa: E501
        :type: str
        """

        self._input_format = input_format

    @property
    def item_id(self):
        """Gets the item_id of this Encrypt.  # noqa: E501

        The item id of the key to use in the encryption process  # noqa: E501

        :return: The item_id of this Encrypt.  # noqa: E501
        :rtype: int
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        """Sets the item_id of this Encrypt.

        The item id of the key to use in the encryption process  # noqa: E501

        :param item_id: The item_id of this Encrypt.  # noqa: E501
        :type: int
        """

        self._item_id = item_id

    @property
    def json(self):
        """Gets the json of this Encrypt.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this Encrypt.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this Encrypt.

        Set output format to JSON  # noqa: E501

        :param json: The json of this Encrypt.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def key_name(self):
        """Gets the key_name of this Encrypt.  # noqa: E501

        The name of the key to use in the encryption process  # noqa: E501

        :return: The key_name of this Encrypt.  # noqa: E501
        :rtype: str
        """
        return self._key_name

    @key_name.setter
    def key_name(self, key_name):
        """Sets the key_name of this Encrypt.

        The name of the key to use in the encryption process  # noqa: E501

        :param key_name: The key_name of this Encrypt.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and key_name is None:  # noqa: E501
            raise ValueError("Invalid value for `key_name`, must not be `None`")  # noqa: E501

        self._key_name = key_name

    @property
    def plaintext(self):
        """Gets the plaintext of this Encrypt.  # noqa: E501

        Data to be encrypted  # noqa: E501

        :return: The plaintext of this Encrypt.  # noqa: E501
        :rtype: str
        """
        return self._plaintext

    @plaintext.setter
    def plaintext(self, plaintext):
        """Sets the plaintext of this Encrypt.

        Data to be encrypted  # noqa: E501

        :param plaintext: The plaintext of this Encrypt.  # noqa: E501
        :type: str
        """

        self._plaintext = plaintext

    @property
    def token(self):
        """Gets the token of this Encrypt.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this Encrypt.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this Encrypt.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this Encrypt.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this Encrypt.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this Encrypt.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this Encrypt.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this Encrypt.  # noqa: E501
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
        if not isinstance(other, Encrypt):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Encrypt):
            return True

        return self.to_dict() != other.to_dict()
