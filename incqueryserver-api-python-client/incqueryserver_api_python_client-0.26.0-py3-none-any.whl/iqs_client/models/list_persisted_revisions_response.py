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


class ListPersistedRevisionsResponse(object):
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
        'persisted_revisions': 'list[RevisionDescriptor]'
    }

    attribute_map = {
        'persisted_revisions': 'persistedRevisions'
    }

    def __init__(self, persisted_revisions=None, local_vars_configuration=None):  # noqa: E501
        """ListPersistedRevisionsResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._persisted_revisions = None
        self.discriminator = None

        self.persisted_revisions = persisted_revisions

    @property
    def persisted_revisions(self):
        """Gets the persisted_revisions of this ListPersistedRevisionsResponse.  # noqa: E501

        List of revision descriptors   # noqa: E501

        :return: The persisted_revisions of this ListPersistedRevisionsResponse.  # noqa: E501
        :rtype: list[RevisionDescriptor]
        """
        return self._persisted_revisions

    @persisted_revisions.setter
    def persisted_revisions(self, persisted_revisions):
        """Sets the persisted_revisions of this ListPersistedRevisionsResponse.

        List of revision descriptors   # noqa: E501

        :param persisted_revisions: The persisted_revisions of this ListPersistedRevisionsResponse.  # noqa: E501
        :type: list[RevisionDescriptor]
        """
        if self.local_vars_configuration.client_side_validation and persisted_revisions is None:  # noqa: E501
            raise ValueError("Invalid value for `persisted_revisions`, must not be `None`")  # noqa: E501

        self._persisted_revisions = persisted_revisions

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
        if not isinstance(other, ListPersistedRevisionsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ListPersistedRevisionsResponse):
            return True

        return self.to_dict() != other.to_dict()
