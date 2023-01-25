"""A command line interface to push a message for consumption"""

import argparse
import logging
import sys

# from typing import Optional
import xml.etree.ElementTree as ET

from .pusher import Pusher
from . import connection_utils, utils

_ENVARS_MAPPING = {
    "CONSUMER_INI_FILE": "INI_FILE",
    "CONSUMER_INI_SECTION": "INI_SECTION",
    "CONSUMER_LOG_FILE": "LOG_FILE",
    "CONSUMER_LOG_LEVEL": "LOG_LEVEL",
}

_LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def __create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and populated the argparse.ArgumentParser for this executable.
    """
    parser = argparse.ArgumentParser(
        description="Executes an instance of a rabbit_consume.pusher class"
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="DEBUG",
        help="print out detail information to stdout, automatically set log level to DEBUG.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--log_file",
        dest="LOG_FILE",
        help="The file, as opposed to stdout, into which to write log messages",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        dest="LOG_LEVEL",
        help="The logging level for this execution",
        choices=_LOG_LEVELS.keys(),
    )
    parser.add_argument(
        "-i",
        "--rabbit_ini",
        dest="INI_FILE",
        help="The path to the file containing the RabbitMQ INI file, the default is"
        + " $HOME/.rabbitMQ.ini",
    )
    parser.add_argument(
        "-s",
        "--ini_section",
        dest="INI_SECTION",
        help='The section of the INI file to use for this execution, the default is "RabbitMQ"',
        default="RabbitMQ",
    )
    parser.add_argument(
        "-t",
        "--transient",
        dest="TRANSIENT",
        help="true if the specified message is transient rather than durable.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "queue", help="The rabbitMQ queue which this client should consume"
    )
    parser.add_argument(
        "message",
        help="The path to the file containing the to be pushed.",
    )
    return parser


def main():
    """
    A command line interface to run a Consumer instance.
    """
    parser = __create_argument_parser()
    envar_values = utils.read_envar_values(_ENVARS_MAPPING)
    options = parser.parse_args(namespace=envar_values)

    if None is options.LOG_FILE:
        logging.basicConfig(stream=sys.stdout, level=_LOG_LEVELS[options.LOG_LEVEL])
    else:
        logging.basicConfig(
            filename=options.LOG_FILE, level=_LOG_LEVELS[options.LOG_LEVEL]
        )

    logging.debug("Begin options:")
    for option in options.__dict__:
        if options.__dict__[option] is not None:
            logging.debug("    %s = %s", option, options.__dict__[option])
    logging.debug("End options:")

    ini_file = utils.find_config(options.INI_FILE)
    connection_parameters = connection_utils.select_connection_parameters(
        ini_file, options.INI_SECTION
    )

    message_content = ET.parse(options.message)
    message = ET.tostring(message_content.getroot())
    pusher = Pusher(
        connection_parameters,
        options.queue,
        durable=not options.TRANSIENT,
    )
    pusher.connect()
    pusher.push(message)
    pusher.close_connection()
