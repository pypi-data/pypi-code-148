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


class EmailAlertSettingsRequest(object):
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
        'progress_percent': 'int',
        'enabled': 'bool',
        'event_types': 'list[EventTypesEnum]'
    }

    attribute_map = {
        'progress_percent': 'progress_percent',
        'enabled': 'enabled',
        'event_types': 'event_types'
    }

    def __init__(self, progress_percent=None, enabled=None, event_types=None, local_vars_configuration=None):  # noqa: E501
        """EmailAlertSettingsRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._progress_percent = None
        self._enabled = None
        self._event_types = None
        self.discriminator = None

        if progress_percent is not None:
            self.progress_percent = progress_percent
        if enabled is not None:
            self.enabled = enabled
        if event_types is not None:
            self.event_types = event_types

    @property
    def progress_percent(self):
        """Gets the progress_percent of this EmailAlertSettingsRequest.  # noqa: E501


        :return: The progress_percent of this EmailAlertSettingsRequest.  # noqa: E501
        :rtype: int
        """
        return self._progress_percent

    @progress_percent.setter
    def progress_percent(self, progress_percent):
        """Sets the progress_percent of this EmailAlertSettingsRequest.


        :param progress_percent: The progress_percent of this EmailAlertSettingsRequest.  # noqa: E501
        :type progress_percent: int
        """
        if (self.local_vars_configuration.client_side_validation and
                progress_percent is not None and progress_percent > 2147483647):  # noqa: E501
            raise ValueError("Invalid value for `progress_percent`, must be a value less than or equal to `2147483647`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                progress_percent is not None and progress_percent < -2147483648):  # noqa: E501
            raise ValueError("Invalid value for `progress_percent`, must be a value greater than or equal to `-2147483648`")  # noqa: E501

        self._progress_percent = progress_percent

    @property
    def enabled(self):
        """Gets the enabled of this EmailAlertSettingsRequest.  # noqa: E501


        :return: The enabled of this EmailAlertSettingsRequest.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this EmailAlertSettingsRequest.


        :param enabled: The enabled of this EmailAlertSettingsRequest.  # noqa: E501
        :type enabled: bool
        """

        self._enabled = enabled

    @property
    def event_types(self):
        """Gets the event_types of this EmailAlertSettingsRequest.  # noqa: E501


        :return: The event_types of this EmailAlertSettingsRequest.  # noqa: E501
        :rtype: list[EventTypesEnum]
        """
        return self._event_types

    @event_types.setter
    def event_types(self, event_types):
        """Sets the event_types of this EmailAlertSettingsRequest.


        :param event_types: The event_types of this EmailAlertSettingsRequest.  # noqa: E501
        :type event_types: list[EventTypesEnum]
        """

        self._event_types = event_types

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
        if not isinstance(other, EmailAlertSettingsRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EmailAlertSettingsRequest):
            return True

        return self.to_dict() != other.to_dict()
