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


class CompartmentOperationStateDetails(object):
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
        'message': 'object',
        'operation_state': 'str'
    }

    attribute_map = {
        'message': 'message',
        'operation_state': 'operationState'
    }

    def __init__(self, message=None, operation_state=None, local_vars_configuration=None):  # noqa: E501
        """CompartmentOperationStateDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._message = None
        self._operation_state = None
        self.discriminator = None

        if message is not None:
            self.message = message
        if operation_state is not None:
            self.operation_state = operation_state

    @property
    def message(self):
        """Gets the message of this CompartmentOperationStateDetails.  # noqa: E501


        :return: The message of this CompartmentOperationStateDetails.  # noqa: E501
        :rtype: object
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this CompartmentOperationStateDetails.


        :param message: The message of this CompartmentOperationStateDetails.  # noqa: E501
        :type: object
        """

        self._message = message

    @property
    def operation_state(self):
        """Gets the operation_state of this CompartmentOperationStateDetails.  # noqa: E501


        :return: The operation_state of this CompartmentOperationStateDetails.  # noqa: E501
        :rtype: str
        """
        return self._operation_state

    @operation_state.setter
    def operation_state(self, operation_state):
        """Sets the operation_state of this CompartmentOperationStateDetails.


        :param operation_state: The operation_state of this CompartmentOperationStateDetails.  # noqa: E501
        :type: str
        """
        allowed_values = ["TERMINATED", "STARTING", "IN_PROGRESS", "COMPLETED", "ERROR"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and operation_state not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `operation_state` ({0}), must be one of {1}"  # noqa: E501
                .format(operation_state, allowed_values)
            )

        self._operation_state = operation_state

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
        if not isinstance(other, CompartmentOperationStateDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CompartmentOperationStateDetails):
            return True

        return self.to_dict() != other.to_dict()
