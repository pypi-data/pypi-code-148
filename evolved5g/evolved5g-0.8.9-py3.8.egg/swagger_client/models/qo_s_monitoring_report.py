# coding: utf-8

"""
    NEF_Emulator

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class QoSMonitoringReport(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'dl_delays': 'list[int]',
        'ul_delays': 'list[int]',
        'rt_delays': 'list[int]'
    }

    attribute_map = {
        'dl_delays': 'dlDelays',
        'ul_delays': 'ulDelays',
        'rt_delays': 'rtDelays'
    }

    def __init__(self, dl_delays=None, ul_delays=None, rt_delays=None):  # noqa: E501
        """QoSMonitoringReport - a model defined in Swagger"""  # noqa: E501
        self._dl_delays = None
        self._ul_delays = None
        self._rt_delays = None
        self.discriminator = None
        if dl_delays is not None:
            self.dl_delays = dl_delays
        if ul_delays is not None:
            self.ul_delays = ul_delays
        if rt_delays is not None:
            self.rt_delays = rt_delays

    @property
    def dl_delays(self):
        """Gets the dl_delays of this QoSMonitoringReport.  # noqa: E501

        Downlink packet delay  # noqa: E501

        :return: The dl_delays of this QoSMonitoringReport.  # noqa: E501
        :rtype: list[int]
        """
        return self._dl_delays

    @dl_delays.setter
    def dl_delays(self, dl_delays):
        """Sets the dl_delays of this QoSMonitoringReport.

        Downlink packet delay  # noqa: E501

        :param dl_delays: The dl_delays of this QoSMonitoringReport.  # noqa: E501
        :type: list[int]
        """

        self._dl_delays = dl_delays

    @property
    def ul_delays(self):
        """Gets the ul_delays of this QoSMonitoringReport.  # noqa: E501

        Uplink packet delay  # noqa: E501

        :return: The ul_delays of this QoSMonitoringReport.  # noqa: E501
        :rtype: list[int]
        """
        return self._ul_delays

    @ul_delays.setter
    def ul_delays(self, ul_delays):
        """Sets the ul_delays of this QoSMonitoringReport.

        Uplink packet delay  # noqa: E501

        :param ul_delays: The ul_delays of this QoSMonitoringReport.  # noqa: E501
        :type: list[int]
        """

        self._ul_delays = ul_delays

    @property
    def rt_delays(self):
        """Gets the rt_delays of this QoSMonitoringReport.  # noqa: E501

        Round trip packet delay  # noqa: E501

        :return: The rt_delays of this QoSMonitoringReport.  # noqa: E501
        :rtype: list[int]
        """
        return self._rt_delays

    @rt_delays.setter
    def rt_delays(self, rt_delays):
        """Sets the rt_delays of this QoSMonitoringReport.

        Round trip packet delay  # noqa: E501

        :param rt_delays: The rt_delays of this QoSMonitoringReport.  # noqa: E501
        :type: list[int]
        """

        self._rt_delays = rt_delays

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(QoSMonitoringReport, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QoSMonitoringReport):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
