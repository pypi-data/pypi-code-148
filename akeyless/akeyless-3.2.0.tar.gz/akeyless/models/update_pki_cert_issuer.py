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


class UpdatePKICertIssuer(object):
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
        'add_tag': 'list[str]',
        'allow_any_name': 'bool',
        'allow_subdomains': 'bool',
        'allowed_domains': 'str',
        'allowed_uri_sans': 'str',
        'client_flag': 'bool',
        'code_signing_flag': 'bool',
        'country': 'str',
        'description': 'str',
        'json': 'bool',
        'key_usage': 'str',
        'locality': 'str',
        'metadata': 'str',
        'name': 'str',
        'new_name': 'str',
        'not_enforce_hostnames': 'bool',
        'not_require_cn': 'bool',
        'organizational_units': 'str',
        'organizations': 'str',
        'postal_code': 'str',
        'province': 'str',
        'rm_tag': 'list[str]',
        'server_flag': 'bool',
        'signer_key_name': 'str',
        'street_address': 'str',
        'token': 'str',
        'ttl': 'int',
        'uid_token': 'str'
    }

    attribute_map = {
        'add_tag': 'add-tag',
        'allow_any_name': 'allow-any-name',
        'allow_subdomains': 'allow-subdomains',
        'allowed_domains': 'allowed-domains',
        'allowed_uri_sans': 'allowed-uri-sans',
        'client_flag': 'client-flag',
        'code_signing_flag': 'code-signing-flag',
        'country': 'country',
        'description': 'description',
        'json': 'json',
        'key_usage': 'key-usage',
        'locality': 'locality',
        'metadata': 'metadata',
        'name': 'name',
        'new_name': 'new-name',
        'not_enforce_hostnames': 'not-enforce-hostnames',
        'not_require_cn': 'not-require-cn',
        'organizational_units': 'organizational-units',
        'organizations': 'organizations',
        'postal_code': 'postal-code',
        'province': 'province',
        'rm_tag': 'rm-tag',
        'server_flag': 'server-flag',
        'signer_key_name': 'signer-key-name',
        'street_address': 'street-address',
        'token': 'token',
        'ttl': 'ttl',
        'uid_token': 'uid-token'
    }

    def __init__(self, add_tag=None, allow_any_name=None, allow_subdomains=None, allowed_domains=None, allowed_uri_sans=None, client_flag=None, code_signing_flag=None, country=None, description=None, json=None, key_usage='DigitalSignature,KeyAgreement,KeyEncipherment', locality=None, metadata=None, name=None, new_name=None, not_enforce_hostnames=None, not_require_cn=None, organizational_units=None, organizations=None, postal_code=None, province=None, rm_tag=None, server_flag=None, signer_key_name=None, street_address=None, token=None, ttl=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """UpdatePKICertIssuer - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._add_tag = None
        self._allow_any_name = None
        self._allow_subdomains = None
        self._allowed_domains = None
        self._allowed_uri_sans = None
        self._client_flag = None
        self._code_signing_flag = None
        self._country = None
        self._description = None
        self._json = None
        self._key_usage = None
        self._locality = None
        self._metadata = None
        self._name = None
        self._new_name = None
        self._not_enforce_hostnames = None
        self._not_require_cn = None
        self._organizational_units = None
        self._organizations = None
        self._postal_code = None
        self._province = None
        self._rm_tag = None
        self._server_flag = None
        self._signer_key_name = None
        self._street_address = None
        self._token = None
        self._ttl = None
        self._uid_token = None
        self.discriminator = None

        if add_tag is not None:
            self.add_tag = add_tag
        if allow_any_name is not None:
            self.allow_any_name = allow_any_name
        if allow_subdomains is not None:
            self.allow_subdomains = allow_subdomains
        if allowed_domains is not None:
            self.allowed_domains = allowed_domains
        if allowed_uri_sans is not None:
            self.allowed_uri_sans = allowed_uri_sans
        if client_flag is not None:
            self.client_flag = client_flag
        if code_signing_flag is not None:
            self.code_signing_flag = code_signing_flag
        if country is not None:
            self.country = country
        if description is not None:
            self.description = description
        if json is not None:
            self.json = json
        if key_usage is not None:
            self.key_usage = key_usage
        if locality is not None:
            self.locality = locality
        if metadata is not None:
            self.metadata = metadata
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if not_enforce_hostnames is not None:
            self.not_enforce_hostnames = not_enforce_hostnames
        if not_require_cn is not None:
            self.not_require_cn = not_require_cn
        if organizational_units is not None:
            self.organizational_units = organizational_units
        if organizations is not None:
            self.organizations = organizations
        if postal_code is not None:
            self.postal_code = postal_code
        if province is not None:
            self.province = province
        if rm_tag is not None:
            self.rm_tag = rm_tag
        if server_flag is not None:
            self.server_flag = server_flag
        self.signer_key_name = signer_key_name
        if street_address is not None:
            self.street_address = street_address
        if token is not None:
            self.token = token
        self.ttl = ttl
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def add_tag(self):
        """Gets the add_tag of this UpdatePKICertIssuer.  # noqa: E501

        List of the new tags that will be attached to this item  # noqa: E501

        :return: The add_tag of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: list[str]
        """
        return self._add_tag

    @add_tag.setter
    def add_tag(self, add_tag):
        """Sets the add_tag of this UpdatePKICertIssuer.

        List of the new tags that will be attached to this item  # noqa: E501

        :param add_tag: The add_tag of this UpdatePKICertIssuer.  # noqa: E501
        :type: list[str]
        """

        self._add_tag = add_tag

    @property
    def allow_any_name(self):
        """Gets the allow_any_name of this UpdatePKICertIssuer.  # noqa: E501

        If set, clients can request certificates for any CN  # noqa: E501

        :return: The allow_any_name of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._allow_any_name

    @allow_any_name.setter
    def allow_any_name(self, allow_any_name):
        """Sets the allow_any_name of this UpdatePKICertIssuer.

        If set, clients can request certificates for any CN  # noqa: E501

        :param allow_any_name: The allow_any_name of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._allow_any_name = allow_any_name

    @property
    def allow_subdomains(self):
        """Gets the allow_subdomains of this UpdatePKICertIssuer.  # noqa: E501

        If set, clients can request certificates for subdomains and wildcard subdomains of the allowed domains  # noqa: E501

        :return: The allow_subdomains of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._allow_subdomains

    @allow_subdomains.setter
    def allow_subdomains(self, allow_subdomains):
        """Sets the allow_subdomains of this UpdatePKICertIssuer.

        If set, clients can request certificates for subdomains and wildcard subdomains of the allowed domains  # noqa: E501

        :param allow_subdomains: The allow_subdomains of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._allow_subdomains = allow_subdomains

    @property
    def allowed_domains(self):
        """Gets the allowed_domains of this UpdatePKICertIssuer.  # noqa: E501

        A list of the allowed domains that clients can request to be included in the certificate (in a comma-delimited list)  # noqa: E501

        :return: The allowed_domains of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._allowed_domains

    @allowed_domains.setter
    def allowed_domains(self, allowed_domains):
        """Sets the allowed_domains of this UpdatePKICertIssuer.

        A list of the allowed domains that clients can request to be included in the certificate (in a comma-delimited list)  # noqa: E501

        :param allowed_domains: The allowed_domains of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._allowed_domains = allowed_domains

    @property
    def allowed_uri_sans(self):
        """Gets the allowed_uri_sans of this UpdatePKICertIssuer.  # noqa: E501

        A list of the allowed URIs that clients can request to be included in the certificate as part of the URI Subject Alternative Names (in a comma-delimited list)  # noqa: E501

        :return: The allowed_uri_sans of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._allowed_uri_sans

    @allowed_uri_sans.setter
    def allowed_uri_sans(self, allowed_uri_sans):
        """Sets the allowed_uri_sans of this UpdatePKICertIssuer.

        A list of the allowed URIs that clients can request to be included in the certificate as part of the URI Subject Alternative Names (in a comma-delimited list)  # noqa: E501

        :param allowed_uri_sans: The allowed_uri_sans of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._allowed_uri_sans = allowed_uri_sans

    @property
    def client_flag(self):
        """Gets the client_flag of this UpdatePKICertIssuer.  # noqa: E501

        If set, certificates will be flagged for client auth use  # noqa: E501

        :return: The client_flag of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._client_flag

    @client_flag.setter
    def client_flag(self, client_flag):
        """Sets the client_flag of this UpdatePKICertIssuer.

        If set, certificates will be flagged for client auth use  # noqa: E501

        :param client_flag: The client_flag of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._client_flag = client_flag

    @property
    def code_signing_flag(self):
        """Gets the code_signing_flag of this UpdatePKICertIssuer.  # noqa: E501

        If set, certificates will be flagged for code signing use  # noqa: E501

        :return: The code_signing_flag of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._code_signing_flag

    @code_signing_flag.setter
    def code_signing_flag(self, code_signing_flag):
        """Sets the code_signing_flag of this UpdatePKICertIssuer.

        If set, certificates will be flagged for code signing use  # noqa: E501

        :param code_signing_flag: The code_signing_flag of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._code_signing_flag = code_signing_flag

    @property
    def country(self):
        """Gets the country of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of the country that will be set in the issued certificate  # noqa: E501

        :return: The country of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this UpdatePKICertIssuer.

        A comma-separated list of the country that will be set in the issued certificate  # noqa: E501

        :param country: The country of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def description(self):
        """Gets the description of this UpdatePKICertIssuer.  # noqa: E501

        Description of the object  # noqa: E501

        :return: The description of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdatePKICertIssuer.

        Description of the object  # noqa: E501

        :param description: The description of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def json(self):
        """Gets the json of this UpdatePKICertIssuer.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this UpdatePKICertIssuer.

        Set output format to JSON  # noqa: E501

        :param json: The json of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def key_usage(self):
        """Gets the key_usage of this UpdatePKICertIssuer.  # noqa: E501

        key-usage  # noqa: E501

        :return: The key_usage of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._key_usage

    @key_usage.setter
    def key_usage(self, key_usage):
        """Sets the key_usage of this UpdatePKICertIssuer.

        key-usage  # noqa: E501

        :param key_usage: The key_usage of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._key_usage = key_usage

    @property
    def locality(self):
        """Gets the locality of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of the locality that will be set in the issued certificate  # noqa: E501

        :return: The locality of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._locality

    @locality.setter
    def locality(self, locality):
        """Sets the locality of this UpdatePKICertIssuer.

        A comma-separated list of the locality that will be set in the issued certificate  # noqa: E501

        :param locality: The locality of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._locality = locality

    @property
    def metadata(self):
        """Gets the metadata of this UpdatePKICertIssuer.  # noqa: E501

        Deprecated - use description  # noqa: E501

        :return: The metadata of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this UpdatePKICertIssuer.

        Deprecated - use description  # noqa: E501

        :param metadata: The metadata of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._metadata = metadata

    @property
    def name(self):
        """Gets the name of this UpdatePKICertIssuer.  # noqa: E501

        PKI certificate issuer name  # noqa: E501

        :return: The name of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdatePKICertIssuer.

        PKI certificate issuer name  # noqa: E501

        :param name: The name of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this UpdatePKICertIssuer.  # noqa: E501

        New item name  # noqa: E501

        :return: The new_name of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this UpdatePKICertIssuer.

        New item name  # noqa: E501

        :param new_name: The new_name of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def not_enforce_hostnames(self):
        """Gets the not_enforce_hostnames of this UpdatePKICertIssuer.  # noqa: E501

        If set, any names are allowed for CN and SANs in the certificate and not only a valid host name  # noqa: E501

        :return: The not_enforce_hostnames of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._not_enforce_hostnames

    @not_enforce_hostnames.setter
    def not_enforce_hostnames(self, not_enforce_hostnames):
        """Sets the not_enforce_hostnames of this UpdatePKICertIssuer.

        If set, any names are allowed for CN and SANs in the certificate and not only a valid host name  # noqa: E501

        :param not_enforce_hostnames: The not_enforce_hostnames of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._not_enforce_hostnames = not_enforce_hostnames

    @property
    def not_require_cn(self):
        """Gets the not_require_cn of this UpdatePKICertIssuer.  # noqa: E501

        If set, clients can request certificates without a CN  # noqa: E501

        :return: The not_require_cn of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._not_require_cn

    @not_require_cn.setter
    def not_require_cn(self, not_require_cn):
        """Sets the not_require_cn of this UpdatePKICertIssuer.

        If set, clients can request certificates without a CN  # noqa: E501

        :param not_require_cn: The not_require_cn of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._not_require_cn = not_require_cn

    @property
    def organizational_units(self):
        """Gets the organizational_units of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of organizational units (OU) that will be set in the issued certificate  # noqa: E501

        :return: The organizational_units of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._organizational_units

    @organizational_units.setter
    def organizational_units(self, organizational_units):
        """Sets the organizational_units of this UpdatePKICertIssuer.

        A comma-separated list of organizational units (OU) that will be set in the issued certificate  # noqa: E501

        :param organizational_units: The organizational_units of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._organizational_units = organizational_units

    @property
    def organizations(self):
        """Gets the organizations of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of organizations (O) that will be set in the issued certificate  # noqa: E501

        :return: The organizations of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._organizations

    @organizations.setter
    def organizations(self, organizations):
        """Sets the organizations of this UpdatePKICertIssuer.

        A comma-separated list of organizations (O) that will be set in the issued certificate  # noqa: E501

        :param organizations: The organizations of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._organizations = organizations

    @property
    def postal_code(self):
        """Gets the postal_code of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of the postal code that will be set in the issued certificate  # noqa: E501

        :return: The postal_code of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """Sets the postal_code of this UpdatePKICertIssuer.

        A comma-separated list of the postal code that will be set in the issued certificate  # noqa: E501

        :param postal_code: The postal_code of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._postal_code = postal_code

    @property
    def province(self):
        """Gets the province of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of the province that will be set in the issued certificate  # noqa: E501

        :return: The province of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._province

    @province.setter
    def province(self, province):
        """Sets the province of this UpdatePKICertIssuer.

        A comma-separated list of the province that will be set in the issued certificate  # noqa: E501

        :param province: The province of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._province = province

    @property
    def rm_tag(self):
        """Gets the rm_tag of this UpdatePKICertIssuer.  # noqa: E501

        List of the existent tags that will be removed from this item  # noqa: E501

        :return: The rm_tag of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: list[str]
        """
        return self._rm_tag

    @rm_tag.setter
    def rm_tag(self, rm_tag):
        """Sets the rm_tag of this UpdatePKICertIssuer.

        List of the existent tags that will be removed from this item  # noqa: E501

        :param rm_tag: The rm_tag of this UpdatePKICertIssuer.  # noqa: E501
        :type: list[str]
        """

        self._rm_tag = rm_tag

    @property
    def server_flag(self):
        """Gets the server_flag of this UpdatePKICertIssuer.  # noqa: E501

        If set, certificates will be flagged for server auth use  # noqa: E501

        :return: The server_flag of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: bool
        """
        return self._server_flag

    @server_flag.setter
    def server_flag(self, server_flag):
        """Sets the server_flag of this UpdatePKICertIssuer.

        If set, certificates will be flagged for server auth use  # noqa: E501

        :param server_flag: The server_flag of this UpdatePKICertIssuer.  # noqa: E501
        :type: bool
        """

        self._server_flag = server_flag

    @property
    def signer_key_name(self):
        """Gets the signer_key_name of this UpdatePKICertIssuer.  # noqa: E501

        A key to sign the certificate with  # noqa: E501

        :return: The signer_key_name of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._signer_key_name

    @signer_key_name.setter
    def signer_key_name(self, signer_key_name):
        """Sets the signer_key_name of this UpdatePKICertIssuer.

        A key to sign the certificate with  # noqa: E501

        :param signer_key_name: The signer_key_name of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and signer_key_name is None:  # noqa: E501
            raise ValueError("Invalid value for `signer_key_name`, must not be `None`")  # noqa: E501

        self._signer_key_name = signer_key_name

    @property
    def street_address(self):
        """Gets the street_address of this UpdatePKICertIssuer.  # noqa: E501

        A comma-separated list of the street address that will be set in the issued certificate  # noqa: E501

        :return: The street_address of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._street_address

    @street_address.setter
    def street_address(self, street_address):
        """Sets the street_address of this UpdatePKICertIssuer.

        A comma-separated list of the street address that will be set in the issued certificate  # noqa: E501

        :param street_address: The street_address of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._street_address = street_address

    @property
    def token(self):
        """Gets the token of this UpdatePKICertIssuer.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdatePKICertIssuer.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdatePKICertIssuer.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def ttl(self):
        """Gets the ttl of this UpdatePKICertIssuer.  # noqa: E501

        he requested Time To Live for the certificate, in seconds  # noqa: E501

        :return: The ttl of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this UpdatePKICertIssuer.

        he requested Time To Live for the certificate, in seconds  # noqa: E501

        :param ttl: The ttl of this UpdatePKICertIssuer.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and ttl is None:  # noqa: E501
            raise ValueError("Invalid value for `ttl`, must not be `None`")  # noqa: E501

        self._ttl = ttl

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdatePKICertIssuer.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdatePKICertIssuer.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdatePKICertIssuer.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdatePKICertIssuer.  # noqa: E501
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
        if not isinstance(other, UpdatePKICertIssuer):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdatePKICertIssuer):
            return True

        return self.to_dict() != other.to_dict()
