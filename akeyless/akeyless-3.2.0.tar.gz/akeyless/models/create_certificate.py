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


class CreateCertificate(object):
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
        'certificate_data': 'str',
        'delete_protection': 'str',
        'description': 'str',
        'expiration_event_in': 'list[str]',
        'json': 'bool',
        'key': 'str',
        'key_data': 'str',
        'metadata': 'str',
        'name': 'str',
        'tags': 'list[str]',
        'token': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'certificate_data': 'certificate-data',
        'delete_protection': 'delete_protection',
        'description': 'description',
        'expiration_event_in': 'expiration-event-in',
        'json': 'json',
        'key': 'key',
        'key_data': 'key-data',
        'metadata': 'metadata',
        'name': 'name',
        'tags': 'tags',
        'token': 'token',
        'uid_token': 'uid-token'
    }

    def __init__(self, certificate_data=None, delete_protection=None, description=None, expiration_event_in=None, json=None, key=None, key_data=None, metadata=None, name=None, tags=None, token=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """CreateCertificate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._certificate_data = None
        self._delete_protection = None
        self._description = None
        self._expiration_event_in = None
        self._json = None
        self._key = None
        self._key_data = None
        self._metadata = None
        self._name = None
        self._tags = None
        self._token = None
        self._uid_token = None
        self.discriminator = None

        if certificate_data is not None:
            self.certificate_data = certificate_data
        if delete_protection is not None:
            self.delete_protection = delete_protection
        if description is not None:
            self.description = description
        if expiration_event_in is not None:
            self.expiration_event_in = expiration_event_in
        if json is not None:
            self.json = json
        if key is not None:
            self.key = key
        if key_data is not None:
            self.key_data = key_data
        if metadata is not None:
            self.metadata = metadata
        self.name = name
        if tags is not None:
            self.tags = tags
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def certificate_data(self):
        """Gets the certificate_data of this CreateCertificate.  # noqa: E501

        Content of the certificate PEM in a Base64 format.  # noqa: E501

        :return: The certificate_data of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._certificate_data

    @certificate_data.setter
    def certificate_data(self, certificate_data):
        """Sets the certificate_data of this CreateCertificate.

        Content of the certificate PEM in a Base64 format.  # noqa: E501

        :param certificate_data: The certificate_data of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._certificate_data = certificate_data

    @property
    def delete_protection(self):
        """Gets the delete_protection of this CreateCertificate.  # noqa: E501

        Protection from accidental deletion of this item  # noqa: E501

        :return: The delete_protection of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._delete_protection

    @delete_protection.setter
    def delete_protection(self, delete_protection):
        """Sets the delete_protection of this CreateCertificate.

        Protection from accidental deletion of this item  # noqa: E501

        :param delete_protection: The delete_protection of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._delete_protection = delete_protection

    @property
    def description(self):
        """Gets the description of this CreateCertificate.  # noqa: E501

        Description of the object  # noqa: E501

        :return: The description of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateCertificate.

        Description of the object  # noqa: E501

        :param description: The description of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def expiration_event_in(self):
        """Gets the expiration_event_in of this CreateCertificate.  # noqa: E501

        How many days before the expiration of the certificate would you like to be notified.  # noqa: E501

        :return: The expiration_event_in of this CreateCertificate.  # noqa: E501
        :rtype: list[str]
        """
        return self._expiration_event_in

    @expiration_event_in.setter
    def expiration_event_in(self, expiration_event_in):
        """Sets the expiration_event_in of this CreateCertificate.

        How many days before the expiration of the certificate would you like to be notified.  # noqa: E501

        :param expiration_event_in: The expiration_event_in of this CreateCertificate.  # noqa: E501
        :type: list[str]
        """

        self._expiration_event_in = expiration_event_in

    @property
    def json(self):
        """Gets the json of this CreateCertificate.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this CreateCertificate.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this CreateCertificate.

        Set output format to JSON  # noqa: E501

        :param json: The json of this CreateCertificate.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def key(self):
        """Gets the key of this CreateCertificate.  # noqa: E501

        The name of a key to use to encrypt the certificate's key (if empty, the account default protectionKey key will be used)  # noqa: E501

        :return: The key of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this CreateCertificate.

        The name of a key to use to encrypt the certificate's key (if empty, the account default protectionKey key will be used)  # noqa: E501

        :param key: The key of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def key_data(self):
        """Gets the key_data of this CreateCertificate.  # noqa: E501

        Content of the certificate's private key PEM in a Base64 format.  # noqa: E501

        :return: The key_data of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._key_data

    @key_data.setter
    def key_data(self, key_data):
        """Sets the key_data of this CreateCertificate.

        Content of the certificate's private key PEM in a Base64 format.  # noqa: E501

        :param key_data: The key_data of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._key_data = key_data

    @property
    def metadata(self):
        """Gets the metadata of this CreateCertificate.  # noqa: E501

        Deprecated - use description  # noqa: E501

        :return: The metadata of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this CreateCertificate.

        Deprecated - use description  # noqa: E501

        :param metadata: The metadata of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this CreateCertificate.  # noqa: E501

        Certificate name  # noqa: E501

        :return: The name of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateCertificate.

        Certificate name  # noqa: E501

        :param name: The name of this CreateCertificate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def tags(self):
        """Gets the tags of this CreateCertificate.  # noqa: E501

        List of the tags attached to this certificate  # noqa: E501

        :return: The tags of this CreateCertificate.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateCertificate.

        List of the tags attached to this certificate  # noqa: E501

        :param tags: The tags of this CreateCertificate.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def token(self):
        """Gets the token of this CreateCertificate.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this CreateCertificate.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this CreateCertificate.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this CreateCertificate.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this CreateCertificate.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this CreateCertificate.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this CreateCertificate.  # noqa: E501
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
        if not isinstance(other, CreateCertificate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateCertificate):
            return True

        return self.to_dict() != other.to_dict()
