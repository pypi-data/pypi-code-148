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


class CreateAuthMethodOIDC(object):
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
        'access_expires': 'int',
        'allowed_redirect_uri': 'list[str]',
        'audience': 'str',
        'bound_ips': 'list[str]',
        'client_id': 'str',
        'client_secret': 'str',
        'force_sub_claims': 'bool',
        'gw_bound_ips': 'list[str]',
        'issuer': 'str',
        'json': 'bool',
        'jwt_ttl': 'int',
        'name': 'str',
        'required_scopes': 'list[str]',
        'required_scopes_prefix': 'str',
        'token': 'str',
        'uid_token': 'str',
        'unique_identifier': 'str'
    }

    attribute_map = {
        'access_expires': 'access-expires',
        'allowed_redirect_uri': 'allowed-redirect-uri',
        'audience': 'audience',
        'bound_ips': 'bound-ips',
        'client_id': 'client-id',
        'client_secret': 'client-secret',
        'force_sub_claims': 'force-sub-claims',
        'gw_bound_ips': 'gw-bound-ips',
        'issuer': 'issuer',
        'json': 'json',
        'jwt_ttl': 'jwt-ttl',
        'name': 'name',
        'required_scopes': 'required-scopes',
        'required_scopes_prefix': 'required-scopes-prefix',
        'token': 'token',
        'uid_token': 'uid-token',
        'unique_identifier': 'unique-identifier'
    }

    def __init__(self, access_expires=0, allowed_redirect_uri=None, audience=None, bound_ips=None, client_id=None, client_secret=None, force_sub_claims=None, gw_bound_ips=None, issuer=None, json=None, jwt_ttl=None, name=None, required_scopes=None, required_scopes_prefix=None, token=None, uid_token=None, unique_identifier=None, local_vars_configuration=None):  # noqa: E501
        """CreateAuthMethodOIDC - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._access_expires = None
        self._allowed_redirect_uri = None
        self._audience = None
        self._bound_ips = None
        self._client_id = None
        self._client_secret = None
        self._force_sub_claims = None
        self._gw_bound_ips = None
        self._issuer = None
        self._json = None
        self._jwt_ttl = None
        self._name = None
        self._required_scopes = None
        self._required_scopes_prefix = None
        self._token = None
        self._uid_token = None
        self._unique_identifier = None
        self.discriminator = None

        if access_expires is not None:
            self.access_expires = access_expires
        if allowed_redirect_uri is not None:
            self.allowed_redirect_uri = allowed_redirect_uri
        if audience is not None:
            self.audience = audience
        if bound_ips is not None:
            self.bound_ips = bound_ips
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if force_sub_claims is not None:
            self.force_sub_claims = force_sub_claims
        if gw_bound_ips is not None:
            self.gw_bound_ips = gw_bound_ips
        if issuer is not None:
            self.issuer = issuer
        if json is not None:
            self.json = json
        if jwt_ttl is not None:
            self.jwt_ttl = jwt_ttl
        self.name = name
        if required_scopes is not None:
            self.required_scopes = required_scopes
        if required_scopes_prefix is not None:
            self.required_scopes_prefix = required_scopes_prefix
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        self.unique_identifier = unique_identifier

    @property
    def access_expires(self):
        """Gets the access_expires of this CreateAuthMethodOIDC.  # noqa: E501

        Access expiration date in Unix timestamp (select 0 for access without expiry date)  # noqa: E501

        :return: The access_expires of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: int
        """
        return self._access_expires

    @access_expires.setter
    def access_expires(self, access_expires):
        """Sets the access_expires of this CreateAuthMethodOIDC.

        Access expiration date in Unix timestamp (select 0 for access without expiry date)  # noqa: E501

        :param access_expires: The access_expires of this CreateAuthMethodOIDC.  # noqa: E501
        :type: int
        """

        self._access_expires = access_expires

    @property
    def allowed_redirect_uri(self):
        """Gets the allowed_redirect_uri of this CreateAuthMethodOIDC.  # noqa: E501

        Allowed redirect URIs after the authentication  # noqa: E501

        :return: The allowed_redirect_uri of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_redirect_uri

    @allowed_redirect_uri.setter
    def allowed_redirect_uri(self, allowed_redirect_uri):
        """Sets the allowed_redirect_uri of this CreateAuthMethodOIDC.

        Allowed redirect URIs after the authentication  # noqa: E501

        :param allowed_redirect_uri: The allowed_redirect_uri of this CreateAuthMethodOIDC.  # noqa: E501
        :type: list[str]
        """

        self._allowed_redirect_uri = allowed_redirect_uri

    @property
    def audience(self):
        """Gets the audience of this CreateAuthMethodOIDC.  # noqa: E501

        Audience claim to be used as part of the authentication flow. In case set, it must match the one configured on the Identity Provider's Application  # noqa: E501

        :return: The audience of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._audience

    @audience.setter
    def audience(self, audience):
        """Sets the audience of this CreateAuthMethodOIDC.

        Audience claim to be used as part of the authentication flow. In case set, it must match the one configured on the Identity Provider's Application  # noqa: E501

        :param audience: The audience of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._audience = audience

    @property
    def bound_ips(self):
        """Gets the bound_ips of this CreateAuthMethodOIDC.  # noqa: E501

        A CIDR whitelist with the IPs that the access is restricted to  # noqa: E501

        :return: The bound_ips of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_ips

    @bound_ips.setter
    def bound_ips(self, bound_ips):
        """Sets the bound_ips of this CreateAuthMethodOIDC.

        A CIDR whitelist with the IPs that the access is restricted to  # noqa: E501

        :param bound_ips: The bound_ips of this CreateAuthMethodOIDC.  # noqa: E501
        :type: list[str]
        """

        self._bound_ips = bound_ips

    @property
    def client_id(self):
        """Gets the client_id of this CreateAuthMethodOIDC.  # noqa: E501

        Client ID  # noqa: E501

        :return: The client_id of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this CreateAuthMethodOIDC.

        Client ID  # noqa: E501

        :param client_id: The client_id of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def client_secret(self):
        """Gets the client_secret of this CreateAuthMethodOIDC.  # noqa: E501

        Client Secret  # noqa: E501

        :return: The client_secret of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        """Sets the client_secret of this CreateAuthMethodOIDC.

        Client Secret  # noqa: E501

        :param client_secret: The client_secret of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._client_secret = client_secret

    @property
    def force_sub_claims(self):
        """Gets the force_sub_claims of this CreateAuthMethodOIDC.  # noqa: E501

        if true: enforce role-association must include sub claims  # noqa: E501

        :return: The force_sub_claims of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: bool
        """
        return self._force_sub_claims

    @force_sub_claims.setter
    def force_sub_claims(self, force_sub_claims):
        """Sets the force_sub_claims of this CreateAuthMethodOIDC.

        if true: enforce role-association must include sub claims  # noqa: E501

        :param force_sub_claims: The force_sub_claims of this CreateAuthMethodOIDC.  # noqa: E501
        :type: bool
        """

        self._force_sub_claims = force_sub_claims

    @property
    def gw_bound_ips(self):
        """Gets the gw_bound_ips of this CreateAuthMethodOIDC.  # noqa: E501

        A CIDR whitelist with the GW IPs that the access is restricted to  # noqa: E501

        :return: The gw_bound_ips of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: list[str]
        """
        return self._gw_bound_ips

    @gw_bound_ips.setter
    def gw_bound_ips(self, gw_bound_ips):
        """Sets the gw_bound_ips of this CreateAuthMethodOIDC.

        A CIDR whitelist with the GW IPs that the access is restricted to  # noqa: E501

        :param gw_bound_ips: The gw_bound_ips of this CreateAuthMethodOIDC.  # noqa: E501
        :type: list[str]
        """

        self._gw_bound_ips = gw_bound_ips

    @property
    def issuer(self):
        """Gets the issuer of this CreateAuthMethodOIDC.  # noqa: E501

        Issuer URL  # noqa: E501

        :return: The issuer of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this CreateAuthMethodOIDC.

        Issuer URL  # noqa: E501

        :param issuer: The issuer of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._issuer = issuer

    @property
    def json(self):
        """Gets the json of this CreateAuthMethodOIDC.  # noqa: E501

        Set output format to JSON  # noqa: E501

        :return: The json of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: bool
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this CreateAuthMethodOIDC.

        Set output format to JSON  # noqa: E501

        :param json: The json of this CreateAuthMethodOIDC.  # noqa: E501
        :type: bool
        """

        self._json = json

    @property
    def jwt_ttl(self):
        """Gets the jwt_ttl of this CreateAuthMethodOIDC.  # noqa: E501

        Jwt TTL  # noqa: E501

        :return: The jwt_ttl of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: int
        """
        return self._jwt_ttl

    @jwt_ttl.setter
    def jwt_ttl(self, jwt_ttl):
        """Sets the jwt_ttl of this CreateAuthMethodOIDC.

        Jwt TTL  # noqa: E501

        :param jwt_ttl: The jwt_ttl of this CreateAuthMethodOIDC.  # noqa: E501
        :type: int
        """

        self._jwt_ttl = jwt_ttl

    @property
    def name(self):
        """Gets the name of this CreateAuthMethodOIDC.  # noqa: E501

        Auth Method name  # noqa: E501

        :return: The name of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateAuthMethodOIDC.

        Auth Method name  # noqa: E501

        :param name: The name of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def required_scopes(self):
        """Gets the required_scopes of this CreateAuthMethodOIDC.  # noqa: E501

        RequiredScopes is a list of required scopes that the oidc method will request from the oidc provider and the user must approve  # noqa: E501

        :return: The required_scopes of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: list[str]
        """
        return self._required_scopes

    @required_scopes.setter
    def required_scopes(self, required_scopes):
        """Sets the required_scopes of this CreateAuthMethodOIDC.

        RequiredScopes is a list of required scopes that the oidc method will request from the oidc provider and the user must approve  # noqa: E501

        :param required_scopes: The required_scopes of this CreateAuthMethodOIDC.  # noqa: E501
        :type: list[str]
        """

        self._required_scopes = required_scopes

    @property
    def required_scopes_prefix(self):
        """Gets the required_scopes_prefix of this CreateAuthMethodOIDC.  # noqa: E501

        RequiredScopesPrefix is a a prefix to add to all required-scopes when requesting them from the oidc server (for example, azures' Application ID URI)  # noqa: E501

        :return: The required_scopes_prefix of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._required_scopes_prefix

    @required_scopes_prefix.setter
    def required_scopes_prefix(self, required_scopes_prefix):
        """Sets the required_scopes_prefix of this CreateAuthMethodOIDC.

        RequiredScopesPrefix is a a prefix to add to all required-scopes when requesting them from the oidc server (for example, azures' Application ID URI)  # noqa: E501

        :param required_scopes_prefix: The required_scopes_prefix of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._required_scopes_prefix = required_scopes_prefix

    @property
    def token(self):
        """Gets the token of this CreateAuthMethodOIDC.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this CreateAuthMethodOIDC.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this CreateAuthMethodOIDC.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this CreateAuthMethodOIDC.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def unique_identifier(self):
        """Gets the unique_identifier of this CreateAuthMethodOIDC.  # noqa: E501

        A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a \"sub claim\" that contains details uniquely identifying that user. This sub claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.  # noqa: E501

        :return: The unique_identifier of this CreateAuthMethodOIDC.  # noqa: E501
        :rtype: str
        """
        return self._unique_identifier

    @unique_identifier.setter
    def unique_identifier(self, unique_identifier):
        """Sets the unique_identifier of this CreateAuthMethodOIDC.

        A unique identifier (ID) value should be configured for OIDC, OAuth2, LDAP and SAML authentication method types and is usually a value such as the email, username, or upn for example. Whenever a user logs in with a token, these authentication types issue a \"sub claim\" that contains details uniquely identifying that user. This sub claim includes a key containing the ID value that you configured, and is used to distinguish between different users from within the same organization.  # noqa: E501

        :param unique_identifier: The unique_identifier of this CreateAuthMethodOIDC.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and unique_identifier is None:  # noqa: E501
            raise ValueError("Invalid value for `unique_identifier`, must not be `None`")  # noqa: E501

        self._unique_identifier = unique_identifier

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
        if not isinstance(other, CreateAuthMethodOIDC):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateAuthMethodOIDC):
            return True

        return self.to_dict() != other.to_dict()
