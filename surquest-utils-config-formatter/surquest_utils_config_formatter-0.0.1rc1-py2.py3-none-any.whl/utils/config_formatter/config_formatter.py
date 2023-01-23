"""
The pyconfig module contains collection of
objects (DotDict + Config) which helps you
to access configurations in JSON files for
Google Cloud Platform based projects.
"""

import os
import json
from pathlib import Path


class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, "keys"):
                value = DotDict(value)
            self[key] = value


class ConfigFormatter:
    """Config class simplifies interaction with configuration files
    and accessing names of the services within the python scripts
    """

    def __init__(
            self,
            project: str = os.path.join(Path.home(), "config/config.cloud.google.env.{env}.json"),
            services: str = os.path.join(Path.home(), "config/config.cloud.google.services.json"),
            solution: str = os.path.join(Path.home(), "config/config.solution.json"),
            tenants: str = os.path.join(Path.home(), "config/config.tenants.json"),
            naming_patterns: str = os.path.join(Path.home(), "config/naming.patterns.json"),
            environment: str = os.environ.get("ENVIRONMENT", "dev"),
    ):
        """Create instance of the Config class

        :param project: path to the GCP project configuration file
        :type project: str
        :param services: path to the services configuration file (specification of the GCP services)
        :type services: str
        :param solution:  path to the solution configuration file (specification of the application)
        :type solution: str
        :param naming_patterns: path to the naming patterns file
        :type naming_patterns: str
        :param tenants: path to the tenants' specification
        :type tenants: str
        :param environment: acronym of the env (DEV/TEST/PRE/PROD)
        :type environment: str
        """

        self.project = self.load_json_config(
            config=project.format(env=environment)
        ).get("project")
        self.services = self.load_json_config(config=services).get("services")
        self.solution = self.load_json_config(config=solution).get("solution")
        self.tenants = self.load_json_config(config=tenants).get("solution")
        self.naming_patterns = self.load_json_config(config=naming_patterns)
        self.environment = environment
        self.conf = DotDict(
            {
                "project": self.project,
                "services": self.services,
                "solution": self.solution,
            }
        )

    @property
    def config(self):
        """Object property: config"""

        return self.conf

    @classmethod
    def load_json_config(cls, config, path=None):
        """Method loads a json config file.

        :param path: path to the config file directory
        :type path: str
        :param config: config file name
        :type config: str
        :return: configuration dictionary
        :rtype: dict
        """

        if path is None:
            path = cls.get_parent_dir_path()
        full_path = os.path.join(path, config)

        with open(full_path, "r") as file_content:

            content = json.load(file_content)

        return content

    @staticmethod
    def get_parent_dir_path():
        """Method returns the parent directory path of the current file.

        :return: parent directory path
        :rtype: str
        """

        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        return path

    def format_pattern(self, pattern: str):
        """Method formats naming pattern.

        :param pattern: naming pattern
        :type pattern: str

        :example:

        >>> config = Config()
        >>> config.format_pattern(pattern="project.name")

        :return: formatted pattern
        :rtype: str
        """

        naming_pattern = self._get_config_item(name=pattern)
        naming_pattern = naming_pattern.replace("${", "{")

        return naming_pattern.format(**self.conf)

    def _get_config_item(self, name, source="naming_patterns"):
        """Method returns config item by dotted name or list.

        :param item: naming pattern name
        :type item: list|str

        :example:

        >>> config = Config()
        >>> config._get_config_item(name="project.name")
        >>> config._get_config_item(name=["project", "name"])

        :return: config_item
        :rtype: str
        """

        if isinstance(name, str):
            item = name.split(".")
        config_item = getattr(self, source)

        for key in item:

            config_item = config_item.get(key)

            if config_item is None:
                raise KeyError(
                    f"Naming pattern key: `{key}` not found in `{config_item}`"
                )
        return config_item
