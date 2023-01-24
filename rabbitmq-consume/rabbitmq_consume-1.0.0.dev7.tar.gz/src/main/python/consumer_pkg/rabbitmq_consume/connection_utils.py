"""Provide utilities to help with RabbitMQ connection"""

from typing import Optional

import pika

from . import utils as consumer_utils

_CONFIG_STRINGS = ["username", "password", "host", "port", "virtual_host"]
_USERNAME_INDEX = 0
_PASSWORD_INDEX = _USERNAME_INDEX + 1
_HOST_INDEX = _PASSWORD_INDEX + 1
_PORT_INDEX = _HOST_INDEX + 1
_VIRTUAL_HOST_INDEX = _PORT_INDEX + 1
_CONFIG_INTEGERS = [
    "channel_max",
    "connection_attempts",
    "frame_max",
    "heartbeat_timeout",
    "retry_delay",
    "socket_timeout",
]
_CHANNEL_MAX_INDEX = 0
_CONNECTION_ATTEMPTS_INDEX = _CHANNEL_MAX_INDEX + 1
_FRAME_MAX_INDEX = _CONNECTION_ATTEMPTS_INDEX + 1
_HEARTBEAT_TIMEOUT_INDEX = _FRAME_MAX_INDEX + 1
_RETRY_TIMEOUT_INDEX = _HEARTBEAT_TIMEOUT_INDEX + 1
_SOCKET_TIMEOUT_INDEX = _RETRY_TIMEOUT_INDEX + 1
_CONFIG_BOOLS = ["backpressure_detection", "ssl"]
_BACKPRESSURE_DETECTION_INDEX = 0
_SSL_INDEX = _BACKPRESSURE_DETECTION_INDEX + 1

_DEFAULT_HEARTBEAT_TIMEOUT = 580
_DEFAULT_PORT = 5672


def read_config(config_file: str, section: str) -> consumer_utils.Configs:
    """
    Reads the supplied configuration ini file.

    Args:
        config_file: the path to the file containing the
                configuration information.
        section: the section within the file containing the
                configuration for this instance.

    Returns:
        A dict of key-value pairs for the specified section of the
                supplied file.
    """
    return consumer_utils.read_config(
        config_file,
        section,
        booleans=_CONFIG_BOOLS,
        integers=_CONFIG_INTEGERS,
        strings=_CONFIG_STRINGS,
    )


def select_heartbeat_timeout(config: consumer_utils.Configs) -> int:
    """
    Returns the heartbeat timeout config element, of the default value if none specified
    """
    result = select_integer(config, _HEARTBEAT_TIMEOUT_INDEX)
    if None is result:
        return _DEFAULT_HEARTBEAT_TIMEOUT
    return result


def select_integer(config: consumer_utils.Configs, index: int) -> Optional[int]:
    """
    Returns the integer config element for the specified index.
    """
    config_key = _CONFIG_INTEGERS[index]
    if config_key not in config or None is config[config_key]:
        return None
    result = config[config_key]
    if int == type(result):
        return result
    raise ValueError("Wrong type of value for key")


def select_port(config: consumer_utils.Configs) -> int:
    """
    Returns the port config element, of the default value if none specified
    """
    result = select_integer(config, _PORT_INDEX)
    if None is result:
        return _DEFAULT_PORT
    return result


def select_string(config: consumer_utils.Configs, index: int) -> Optional[str]:
    """
    Returns the string config element for the specified index.
    """
    config_key = _CONFIG_STRINGS[index]
    if config_key not in config or None is config[config_key]:
        return None
    result = config[config_key]
    if str == type(result):
        return result
    raise ValueError("Wrong type of value for key")


def select_connection_parameters(config_file: str, section: str):
    """
    Read the config file and creates an appropriate ConnectionParameter instance
    """
    config = read_config(config_file, section)
    username = select_string(config, _USERNAME_INDEX)
    password = select_string(config, _PASSWORD_INDEX)
    if None is username or None is password:
        raise ValueError("Both username and password are required")
    credentials = pika.PlainCredentials(username, password)
    if "port" not in config:
        config["port"] = 5672
    if "heartbeat_timeout" not in config:
        config["heartbeat_timeout"] = 580
    parameters = pika.ConnectionParameters()
    host = select_string(config, _HOST_INDEX)
    if None is not host:
        parameters.host = host
    port = select_port(config)
    if None is not port:
        parameters.port = port
    parameters.credentials = credentials
    virtual_host = select_string(config, _VIRTUAL_HOST_INDEX)
    if None is not virtual_host:
        parameters.virtual_host = virtual_host
    parameters.heartbeat = select_integer(config, _HEARTBEAT_TIMEOUT_INDEX)
    return parameters
