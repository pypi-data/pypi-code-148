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


class DecryptGPG(object):
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
        'ciphertext': 'str',
        'display_id': 'str',
        'item_id': 'int',
        'json': 'bool',
        'key_name': 'str',
        'output_format': 'str',
        'passphrase': 'str',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'ciphertext': 'ciphertext',
        'display_id': 'display-id',
        'item_id': 'item-id',
        'json': 'json',
        'key_name': 'key-name',
        'output_format': 'output-format',
        'passphrase': 'passphrase',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, ciphertext=None, display_id=None, item_id=None, json=None, key_name=None, output_format=None, passphrase=None, token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """DecryptGPG - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._ciphertext = None
        self._display_id = None
        self._item_id = None
        self._json = None
        self._key_name = None
        self._output_format = None
        self._passphrase = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        self.ciphertext = ciphertext
        if display_id is not None:
            self.display_id = display_id
        if item_id is not None:
            self.item_id = item_id
        if json is not None:
            self.json = json
        self.key_name = key_name
        if output_format is not None:
            self.output_format = output_format
        if passphrase is not None:
            self.passphrase = passphrase
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def ciphertext(self):
        """Gets the ciphertext of this DecryptGPG.  # noqa: E501

        Ciphertext to be decrypted in base64 encoded format  # noqa: E501

        :return: The ciphertext of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._ciphertext

    @ciphertext.setter
    def ciphertext(self, ciphertext):
        """Sets the ciphertext of this DecryptGPG.

        Ciphertext to be decrypted in base64 encoded format  # noqa: E501

        :param ciphertext: The ciphertext of this DecryptGPG.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and ciphertext is None:  # noqa: E501
            raise ValueError("Invalid value for `ciphertext`, must not be `None`")  # noqa: E501

        self._ciphertext = ciphertext

    @property
    def display_id(self):
        """Gets the display_id of this DecryptGPG.  # noqa: E501

        The display id of the key to use in the decryption process  # noqa: E501

        :return: The display_id of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._display_id

    @display_id.setter
    def display_id(self, display_id):
        """Sets the display_id of this DecryptGPG.

        The display id of the key to use in the decryption process  # noqa: E501

        :param display_id: The display_id of this DecryptGPG.  # noqa: E501
        :type: str
        """

        self._display_id = display_id

    @property
    def item_id(self):
        """Gets the item_id of this DecryptGPG.  # noqa: E501

        The item id of the key to use in the decryption process  # noqa: E501

        :return: The item_id of this DecryptGPG.  # noqa: E501
        :rtype: int
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        """Sets the item_id of this DecryptGPG.

        The item id of the key to use in the decryption process  # noqa: E501

        :param item_id: The item_id of this DecryptGPG.  # noqa: E501
        :type: int
        """

        self._item_id = item_id

    @property
    def json(self):
        """Gets the json of this DecryptGPG.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this DecryptGPG.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this DecryptGPG.

        Set output format to JSON  # noqa: E501

        :param json: The json of this DecryptGPG.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def key_name(self):
        """Gets the key_name of this DecryptGPG.  # noqa: E501

        The name of the key to use in the decryption process  # noqa: E501

        :return: The key_name of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._key_name

    @key_name.setter
    def key_name(self, key_name):
        """Sets the key_name of this DecryptGPG.

        The name of the key to use in the decryption process  # noqa: E501

        :param key_name: The key_name of this DecryptGPG.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and key_name is None:  # noqa: E501
            raise ValueError("Invalid value for `key_name`, must not be `None`")  # noqa: E501

        self._key_name = key_name

    @property
    def output_format(self):
        """Gets the output_format of this DecryptGPG.  # noqa: E501

        If specified, the output will be formatted accordingly. options: [base64]  # noqa: E501

        :return: The output_format of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._output_format

    @output_format.setter
    def output_format(self, output_format):
        """Sets the output_format of this DecryptGPG.

        If specified, the output will be formatted accordingly. options: [base64]  # noqa: E501

        :param output_format: The output_format of this DecryptGPG.  # noqa: E501
        :type: str
        """

        self._output_format = output_format

    @property
    def passphrase(self):
        """Gets the passphrase of this DecryptGPG.  # noqa: E501

        Passphrase that was used to generate the key  # noqa: E501

        :return: The passphrase of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._passphrase

    @passphrase.setter
    def passphrase(self, passphrase):
        """Sets the passphrase of this DecryptGPG.

        Passphrase that was used to generate the key  # noqa: E501

        :param passphrase: The passphrase of this DecryptGPG.  # noqa: E501
        :type: str
        """

        self._passphrase = passphrase

    @property
    def token(self):
        """Gets the token of this DecryptGPG.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this DecryptGPG.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this DecryptGPG.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this DecryptGPG.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this DecryptGPG.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this DecryptGPG.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this DecryptGPG.  # noqa: E501
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
        if not isinstance(other, DecryptGPG):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DecryptGPG):
            return True

        return self.to_dict() != other.to_dict()
