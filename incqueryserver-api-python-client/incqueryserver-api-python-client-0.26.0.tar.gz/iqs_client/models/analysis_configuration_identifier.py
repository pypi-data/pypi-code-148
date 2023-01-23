# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: placeHolderApiVersion
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from iqs_client.configuration import Configuration


class AnalysisConfigurationIdentifier(object):
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
        'configuration_id': 'str',
        'configuration_name': 'str'
    }

    attribute_map = {
        'configuration_id': 'configurationId',
        'configuration_name': 'configurationName'
    }

    def __init__(self, configuration_id=None, configuration_name=None, local_vars_configuration=None):  # noqa: E501
        """AnalysisConfigurationIdentifier - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._configuration_id = None
        self._configuration_name = None
        self.discriminator = None

        self.configuration_id = configuration_id
        if configuration_name is not None:
            self.configuration_name = configuration_name

    @property
    def configuration_id(self):
        """Gets the configuration_id of this AnalysisConfigurationIdentifier.  # noqa: E501


        :return: The configuration_id of this AnalysisConfigurationIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._configuration_id

    @configuration_id.setter
    def configuration_id(self, configuration_id):
        """Sets the configuration_id of this AnalysisConfigurationIdentifier.


        :param configuration_id: The configuration_id of this AnalysisConfigurationIdentifier.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and configuration_id is None:  # noqa: E501
            raise ValueError("Invalid value for `configuration_id`, must not be `None`")  # noqa: E501

        self._configuration_id = configuration_id

    @property
    def configuration_name(self):
        """Gets the configuration_name of this AnalysisConfigurationIdentifier.  # noqa: E501


        :return: The configuration_name of this AnalysisConfigurationIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._configuration_name

    @configuration_name.setter
    def configuration_name(self, configuration_name):
        """Sets the configuration_name of this AnalysisConfigurationIdentifier.


        :param configuration_name: The configuration_name of this AnalysisConfigurationIdentifier.  # noqa: E501
        :type: str
        """

        self._configuration_name = configuration_name

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
        if not isinstance(other, AnalysisConfigurationIdentifier):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AnalysisConfigurationIdentifier):
            return True

        return self.to_dict() != other.to_dict()
