# Copyright 2022 The KServe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    KServe

    Python SDK for KServe  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kserve.configuration import Configuration


class V1alpha1Container(object):
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
        'args': 'list[str]',
        'command': 'list[str]',
        'env': 'list[V1EnvVar]',
        'image': 'str',
        'image_pull_policy': 'str',
        'liveness_probe': 'V1Probe',
        'name': 'str',
        'readiness_probe': 'V1Probe',
        'resources': 'V1ResourceRequirements',
        'working_dir': 'str'
    }

    attribute_map = {
        'args': 'args',
        'command': 'command',
        'env': 'env',
        'image': 'image',
        'image_pull_policy': 'imagePullPolicy',
        'liveness_probe': 'livenessProbe',
        'name': 'name',
        'readiness_probe': 'readinessProbe',
        'resources': 'resources',
        'working_dir': 'workingDir'
    }

    def __init__(self, args=None, command=None, env=None, image=None, image_pull_policy=None, liveness_probe=None, name=None, readiness_probe=None, resources=None, working_dir=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha1Container - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._args = None
        self._command = None
        self._env = None
        self._image = None
        self._image_pull_policy = None
        self._liveness_probe = None
        self._name = None
        self._readiness_probe = None
        self._resources = None
        self._working_dir = None
        self.discriminator = None

        if args is not None:
            self.args = args
        if command is not None:
            self.command = command
        if env is not None:
            self.env = env
        if image is not None:
            self.image = image
        if image_pull_policy is not None:
            self.image_pull_policy = image_pull_policy
        if liveness_probe is not None:
            self.liveness_probe = liveness_probe
        if name is not None:
            self.name = name
        if readiness_probe is not None:
            self.readiness_probe = readiness_probe
        if resources is not None:
            self.resources = resources
        if working_dir is not None:
            self.working_dir = working_dir

    @property
    def args(self):
        """Gets the args of this V1alpha1Container.  # noqa: E501


        :return: The args of this V1alpha1Container.  # noqa: E501
        :rtype: list[str]
        """
        return self._args

    @args.setter
    def args(self, args):
        """Sets the args of this V1alpha1Container.


        :param args: The args of this V1alpha1Container.  # noqa: E501
        :type: list[str]
        """

        self._args = args

    @property
    def command(self):
        """Gets the command of this V1alpha1Container.  # noqa: E501


        :return: The command of this V1alpha1Container.  # noqa: E501
        :rtype: list[str]
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this V1alpha1Container.


        :param command: The command of this V1alpha1Container.  # noqa: E501
        :type: list[str]
        """

        self._command = command

    @property
    def env(self):
        """Gets the env of this V1alpha1Container.  # noqa: E501


        :return: The env of this V1alpha1Container.  # noqa: E501
        :rtype: list[V1EnvVar]
        """
        return self._env

    @env.setter
    def env(self, env):
        """Sets the env of this V1alpha1Container.


        :param env: The env of this V1alpha1Container.  # noqa: E501
        :type: list[V1EnvVar]
        """

        self._env = env

    @property
    def image(self):
        """Gets the image of this V1alpha1Container.  # noqa: E501


        :return: The image of this V1alpha1Container.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this V1alpha1Container.


        :param image: The image of this V1alpha1Container.  # noqa: E501
        :type: str
        """

        self._image = image

    @property
    def image_pull_policy(self):
        """Gets the image_pull_policy of this V1alpha1Container.  # noqa: E501


        :return: The image_pull_policy of this V1alpha1Container.  # noqa: E501
        :rtype: str
        """
        return self._image_pull_policy

    @image_pull_policy.setter
    def image_pull_policy(self, image_pull_policy):
        """Sets the image_pull_policy of this V1alpha1Container.


        :param image_pull_policy: The image_pull_policy of this V1alpha1Container.  # noqa: E501
        :type: str
        """

        self._image_pull_policy = image_pull_policy

    @property
    def liveness_probe(self):
        """Gets the liveness_probe of this V1alpha1Container.  # noqa: E501


        :return: The liveness_probe of this V1alpha1Container.  # noqa: E501
        :rtype: V1Probe
        """
        return self._liveness_probe

    @liveness_probe.setter
    def liveness_probe(self, liveness_probe):
        """Sets the liveness_probe of this V1alpha1Container.


        :param liveness_probe: The liveness_probe of this V1alpha1Container.  # noqa: E501
        :type: V1Probe
        """

        self._liveness_probe = liveness_probe

    @property
    def name(self):
        """Gets the name of this V1alpha1Container.  # noqa: E501


        :return: The name of this V1alpha1Container.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1alpha1Container.


        :param name: The name of this V1alpha1Container.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def readiness_probe(self):
        """Gets the readiness_probe of this V1alpha1Container.  # noqa: E501


        :return: The readiness_probe of this V1alpha1Container.  # noqa: E501
        :rtype: V1Probe
        """
        return self._readiness_probe

    @readiness_probe.setter
    def readiness_probe(self, readiness_probe):
        """Sets the readiness_probe of this V1alpha1Container.


        :param readiness_probe: The readiness_probe of this V1alpha1Container.  # noqa: E501
        :type: V1Probe
        """

        self._readiness_probe = readiness_probe

    @property
    def resources(self):
        """Gets the resources of this V1alpha1Container.  # noqa: E501


        :return: The resources of this V1alpha1Container.  # noqa: E501
        :rtype: V1ResourceRequirements
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this V1alpha1Container.


        :param resources: The resources of this V1alpha1Container.  # noqa: E501
        :type: V1ResourceRequirements
        """

        self._resources = resources

    @property
    def working_dir(self):
        """Gets the working_dir of this V1alpha1Container.  # noqa: E501


        :return: The working_dir of this V1alpha1Container.  # noqa: E501
        :rtype: str
        """
        return self._working_dir

    @working_dir.setter
    def working_dir(self, working_dir):
        """Sets the working_dir of this V1alpha1Container.


        :param working_dir: The working_dir of this V1alpha1Container.  # noqa: E501
        :type: str
        """

        self._working_dir = working_dir

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
        if not isinstance(other, V1alpha1Container):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha1Container):
            return True

        return self.to_dict() != other.to_dict()
