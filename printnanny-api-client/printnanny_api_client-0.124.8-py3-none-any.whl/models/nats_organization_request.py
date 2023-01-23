# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.124.8
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from printnanny_api_client.configuration import Configuration


class NatsOrganizationRequest(object):
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
        'name': 'str',
        'is_active': 'bool',
        'slug': 'str',
        'json': 'dict(str, object)',
        'jetstream_enabled': 'bool',
        'jetstream_max_mem': 'str',
        'jetstream_max_file': 'str',
        'jetstream_max_streams': 'int',
        'jetstream_max_consumers': 'int',
        'imports': 'list[int]',
        'exports': 'list[int]'
    }

    attribute_map = {
        'name': 'name',
        'is_active': 'is_active',
        'slug': 'slug',
        'json': 'json',
        'jetstream_enabled': 'jetstream_enabled',
        'jetstream_max_mem': 'jetstream_max_mem',
        'jetstream_max_file': 'jetstream_max_file',
        'jetstream_max_streams': 'jetstream_max_streams',
        'jetstream_max_consumers': 'jetstream_max_consumers',
        'imports': 'imports',
        'exports': 'exports'
    }

    def __init__(self, name=None, is_active=None, slug=None, json=None, jetstream_enabled=None, jetstream_max_mem=None, jetstream_max_file=None, jetstream_max_streams=None, jetstream_max_consumers=None, imports=None, exports=None, local_vars_configuration=None):  # noqa: E501
        """NatsOrganizationRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._is_active = None
        self._slug = None
        self._json = None
        self._jetstream_enabled = None
        self._jetstream_max_mem = None
        self._jetstream_max_file = None
        self._jetstream_max_streams = None
        self._jetstream_max_consumers = None
        self._imports = None
        self._exports = None
        self.discriminator = None

        self.name = name
        if is_active is not None:
            self.is_active = is_active
        self.slug = slug
        if json is not None:
            self.json = json
        if jetstream_enabled is not None:
            self.jetstream_enabled = jetstream_enabled
        if jetstream_max_mem is not None:
            self.jetstream_max_mem = jetstream_max_mem
        if jetstream_max_file is not None:
            self.jetstream_max_file = jetstream_max_file
        if jetstream_max_streams is not None:
            self.jetstream_max_streams = jetstream_max_streams
        if jetstream_max_consumers is not None:
            self.jetstream_max_consumers = jetstream_max_consumers
        self.imports = imports
        self.exports = exports

    @property
    def name(self):
        """Gets the name of this NatsOrganizationRequest.  # noqa: E501

        The name of the organization  # noqa: E501

        :return: The name of this NatsOrganizationRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NatsOrganizationRequest.

        The name of the organization  # noqa: E501

        :param name: The name of this NatsOrganizationRequest.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 200):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `200`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def is_active(self):
        """Gets the is_active of this NatsOrganizationRequest.  # noqa: E501


        :return: The is_active of this NatsOrganizationRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this NatsOrganizationRequest.


        :param is_active: The is_active of this NatsOrganizationRequest.  # noqa: E501
        :type is_active: bool
        """

        self._is_active = is_active

    @property
    def slug(self):
        """Gets the slug of this NatsOrganizationRequest.  # noqa: E501

        The name in all lowercase, suitable for URL identification  # noqa: E501

        :return: The slug of this NatsOrganizationRequest.  # noqa: E501
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug):
        """Sets the slug of this NatsOrganizationRequest.

        The name in all lowercase, suitable for URL identification  # noqa: E501

        :param slug: The slug of this NatsOrganizationRequest.  # noqa: E501
        :type slug: str
        """
        if self.local_vars_configuration.client_side_validation and slug is None:  # noqa: E501
            raise ValueError("Invalid value for `slug`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                slug is not None and len(slug) > 200):
            raise ValueError("Invalid value for `slug`, length must be less than or equal to `200`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                slug is not None and len(slug) < 1):
            raise ValueError("Invalid value for `slug`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                slug is not None and not re.search(r'^[-a-zA-Z0-9_]+$', slug)):  # noqa: E501
            raise ValueError(r"Invalid value for `slug`, must be a follow pattern or equal to `/^[-a-zA-Z0-9_]+$/`")  # noqa: E501

        self._slug = slug

    @property
    def json(self):
        """Gets the json of this NatsOrganizationRequest.  # noqa: E501

        Output of `nsc describe account`  # noqa: E501

        :return: The json of this NatsOrganizationRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this NatsOrganizationRequest.

        Output of `nsc describe account`  # noqa: E501

        :param json: The json of this NatsOrganizationRequest.  # noqa: E501
        :type json: dict(str, object)
        """

        self._json = json

    @property
    def jetstream_enabled(self):
        """Gets the jetstream_enabled of this NatsOrganizationRequest.  # noqa: E501

        Enable JetStream for all users/apps belonging to NatsOrganization account  # noqa: E501

        :return: The jetstream_enabled of this NatsOrganizationRequest.  # noqa: E501
        :rtype: bool
        """
        return self._jetstream_enabled

    @jetstream_enabled.setter
    def jetstream_enabled(self, jetstream_enabled):
        """Sets the jetstream_enabled of this NatsOrganizationRequest.

        Enable JetStream for all users/apps belonging to NatsOrganization account  # noqa: E501

        :param jetstream_enabled: The jetstream_enabled of this NatsOrganizationRequest.  # noqa: E501
        :type jetstream_enabled: bool
        """

        self._jetstream_enabled = jetstream_enabled

    @property
    def jetstream_max_mem(self):
        """Gets the jetstream_max_mem of this NatsOrganizationRequest.  # noqa: E501

        JetStream memory resource limits (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :return: The jetstream_max_mem of this NatsOrganizationRequest.  # noqa: E501
        :rtype: str
        """
        return self._jetstream_max_mem

    @jetstream_max_mem.setter
    def jetstream_max_mem(self, jetstream_max_mem):
        """Sets the jetstream_max_mem of this NatsOrganizationRequest.

        JetStream memory resource limits (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :param jetstream_max_mem: The jetstream_max_mem of this NatsOrganizationRequest.  # noqa: E501
        :type jetstream_max_mem: str
        """
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_mem is not None and len(jetstream_max_mem) > 32):
            raise ValueError("Invalid value for `jetstream_max_mem`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_mem is not None and len(jetstream_max_mem) < 1):
            raise ValueError("Invalid value for `jetstream_max_mem`, length must be greater than or equal to `1`")  # noqa: E501

        self._jetstream_max_mem = jetstream_max_mem

    @property
    def jetstream_max_file(self):
        """Gets the jetstream_max_file of this NatsOrganizationRequest.  # noqa: E501

        JetStream file resource limits (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :return: The jetstream_max_file of this NatsOrganizationRequest.  # noqa: E501
        :rtype: str
        """
        return self._jetstream_max_file

    @jetstream_max_file.setter
    def jetstream_max_file(self, jetstream_max_file):
        """Sets the jetstream_max_file of this NatsOrganizationRequest.

        JetStream file resource limits (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :param jetstream_max_file: The jetstream_max_file of this NatsOrganizationRequest.  # noqa: E501
        :type jetstream_max_file: str
        """
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_file is not None and len(jetstream_max_file) > 32):
            raise ValueError("Invalid value for `jetstream_max_file`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_file is not None and len(jetstream_max_file) < 1):
            raise ValueError("Invalid value for `jetstream_max_file`, length must be greater than or equal to `1`")  # noqa: E501

        self._jetstream_max_file = jetstream_max_file

    @property
    def jetstream_max_streams(self):
        """Gets the jetstream_max_streams of this NatsOrganizationRequest.  # noqa: E501

        JetStream max number of streams (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :return: The jetstream_max_streams of this NatsOrganizationRequest.  # noqa: E501
        :rtype: int
        """
        return self._jetstream_max_streams

    @jetstream_max_streams.setter
    def jetstream_max_streams(self, jetstream_max_streams):
        """Sets the jetstream_max_streams of this NatsOrganizationRequest.

        JetStream max number of streams (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :param jetstream_max_streams: The jetstream_max_streams of this NatsOrganizationRequest.  # noqa: E501
        :type jetstream_max_streams: int
        """
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_streams is not None and jetstream_max_streams > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `jetstream_max_streams`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_streams is not None and jetstream_max_streams < 0):  # noqa: E501
            raise ValueError("Invalid value for `jetstream_max_streams`, must be a value greater than or equal to `0`")  # noqa: E501

        self._jetstream_max_streams = jetstream_max_streams

    @property
    def jetstream_max_consumers(self):
        """Gets the jetstream_max_consumers of this NatsOrganizationRequest.  # noqa: E501

        JetStream max number of consumers (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :return: The jetstream_max_consumers of this NatsOrganizationRequest.  # noqa: E501
        :rtype: int
        """
        return self._jetstream_max_consumers

    @jetstream_max_consumers.setter
    def jetstream_max_consumers(self, jetstream_max_consumers):
        """Sets the jetstream_max_consumers of this NatsOrganizationRequest.

        JetStream max number of consumers (shared across all users/apps beloning to NatsOrganization account)  # noqa: E501

        :param jetstream_max_consumers: The jetstream_max_consumers of this NatsOrganizationRequest.  # noqa: E501
        :type jetstream_max_consumers: int
        """
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_consumers is not None and jetstream_max_consumers > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `jetstream_max_consumers`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                jetstream_max_consumers is not None and jetstream_max_consumers < 0):  # noqa: E501
            raise ValueError("Invalid value for `jetstream_max_consumers`, must be a value greater than or equal to `0`")  # noqa: E501

        self._jetstream_max_consumers = jetstream_max_consumers

    @property
    def imports(self):
        """Gets the imports of this NatsOrganizationRequest.  # noqa: E501


        :return: The imports of this NatsOrganizationRequest.  # noqa: E501
        :rtype: list[int]
        """
        return self._imports

    @imports.setter
    def imports(self, imports):
        """Sets the imports of this NatsOrganizationRequest.


        :param imports: The imports of this NatsOrganizationRequest.  # noqa: E501
        :type imports: list[int]
        """
        if self.local_vars_configuration.client_side_validation and imports is None:  # noqa: E501
            raise ValueError("Invalid value for `imports`, must not be `None`")  # noqa: E501

        self._imports = imports

    @property
    def exports(self):
        """Gets the exports of this NatsOrganizationRequest.  # noqa: E501


        :return: The exports of this NatsOrganizationRequest.  # noqa: E501
        :rtype: list[int]
        """
        return self._exports

    @exports.setter
    def exports(self, exports):
        """Sets the exports of this NatsOrganizationRequest.


        :param exports: The exports of this NatsOrganizationRequest.  # noqa: E501
        :type exports: list[int]
        """
        if self.local_vars_configuration.client_side_validation and exports is None:  # noqa: E501
            raise ValueError("Invalid value for `exports`, must not be `None`")  # noqa: E501

        self._exports = exports

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NatsOrganizationRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NatsOrganizationRequest):
            return True

        return self.to_dict() != other.to_dict()
