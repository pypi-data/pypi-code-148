"""Provide utilities to help using the rabbitmq_consume package"""

from argparse import Namespace
from configparser import ConfigParser
import os
from typing import Dict, List, Union

DEFAULT_INI_FILE = "rabbitmq.ini"


Configs = dict[str, Union[bool, int, str, None]]


def find_config(config_file):
    """
    Returns the configuration file depending on the value of the config file passed.
    """
    if None is config_file:
        if "HOME" in os.environ:
            result = os.path.join(os.environ["HOME"], DEFAULT_INI_FILE)
        else:
            raise ValueError(
                "Can not find INI file $HOME/"
                + DEFAULT_INI_FILE
                + ", make sure HOME is defined"
            )
    else:
        result = config_file
    if not os.path.exists(result):
        raise ValueError("Can not find INI file " + result + ", is does not exist")
    return result


def read_envar_values(mapping: Dict[str, str]):
    """
    Create a argparse.Namespace instance populated by the values of the
    envrionmental variables specified by the keys of the mapping.
    """
    result = {}
    for key in mapping.keys():
        value = os.getenv(key)
        if None is not value:
            option = mapping[key]
            result[option] = value
    return Namespace(**result)


def read_config(  # pylint: disable=too-many-arguments, too-many-branches
    config_file: str,
    section: str,
    strings: List[str] = None,
    integers: List[str] = None,
    booleans: List[str] = None,
) -> Configs:
    """
    Reads the supplied configuration ini

    :param config_file: the path to the file containing the configuration information.
    :param section: the section within the file containing the configuration for this instance.
    :param booleans: a List of keys that should be returned as bools.
    :param integers: a List of keys that should be returned as integers.
    """

    config_parser = ConfigParser()
    filepath = find_config(config_file)

    config_parser.read(filepath)
    config: Configs = {}
    for option in config_parser.options(section):
        try:
            if None is not strings and option in strings:
                config[option] = config_parser.get(section, option)
            if None is not integers and option in integers:
                config[option] = config_parser.getint(section, option)
            elif None is not booleans and option in booleans:
                config[option] = config_parser.getboolean(section, option)
            else:
                config[option] = config_parser.get(section, option)
        except:  # pylint: disable=bare-except
            config[option] = None

    if None is not strings:
        for option in strings:
            if not option in config:
                config[option] = None

    if None is not integers:
        for option in integers:
            if not option in config:
                config[option] = None

    if None is not booleans:
        for option in booleans:
            if not option in config:
                config[option] = None

    return config
