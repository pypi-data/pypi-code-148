"""A command line interface to run a Consumer instance"""

import argparse
import logging
import sys
from typing import Optional
import os

from .consumer import Consumer
from . import connection_utils
from . import utils

_ENVARS_MAPPING = {
    "CONSUMER_LIVE_TIME": "LIVE_TIME",
    "CONSUMER_LOG_FILE": "LOG_FILE",
    "CONSUMER_LOG_LEVEL": "LOG_LEVEL",
    "CONSUMER_INI_FILE": "INI_FILE",
    "CONSUMER_RESTART": "RESTART",
    "CONSUMER_INI_SECTION": "INI_SECTION",
    "CONSUMER_TRANSIENT": "TRANSIENT",
    "CONSUMER_WORKERS": "WORKERS",
    "CONSUMER_WAIT_TIME": "WAIT_TIME",
}

_LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def __create_argument_parser(include_consumption: bool) -> argparse.ArgumentParser:
    """
    Creates and populated the argparse.ArgumentParser for this executable.
    """
    parser = argparse.ArgumentParser(
        description="Executes an instance of a rabbit_consume.consumer class"
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
        "--live_time",
        dest="LIVE_TIME",
        help="The number of seconds that this client  should listen for new messages. After this "
        + "time, and once any consumption that was in progress when it expired, the client with "
        + "gracefully exit.",
        type=float,
        default=0.0,
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
        "-r",
        "--restart",
        dest="RESTART",
        help="The number of seconds to wait before attempting to reconnect after a lost connection."
        + " Zero or less means no reconnect will be attempted.",
        type=int,
        default=0,
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
        help="true if the specified queue is transient rather than durable.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-w",
        "--workers",
        dest="WORKERS",
        help="The maximum number of workers that will run in parallel",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--wait_time",
        dest="WAIT_TIME",
        help="The number of seconds that this client should wait with no message after which the "
        + "client with gracefully exit.",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "queue", help="The rabbitMQ queue which this client should consume"
    )
    if include_consumption:
        parser.add_argument(
            dest="consumption_class",
            nargs=1,
            help="The module:Class the implements rabbitmq_consume:Consumption Protocol",
        )
    return parser


def main():
    """
    A command line interface to run a Consumer instance.
    """
    # Test for environmental definition of Consumption class.
    consumption_name: Optional[str] = None
    if "CONSUMER_CONSUMPTION" in os.environ:
        consumption_name = os.environ["CONSUMER_CONSUMPTION"]

    parser = __create_argument_parser(None is consumption_name)
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
    if None is consumption_name:
        consumption_name = options.consumption_class[0]
    logging.info("Consumption done using the %s Class", consumption_name)

    ini_file = utils.find_config(options.INI_FILE)
    connection_parameters = connection_utils.select_connection_parameters(
        ini_file, options.INI_SECTION
    )

    consumer = Consumer(
        connection_parameters,
        options.queue,
        target=consumption_name,
        prefetch=options.WORKERS,
        restart=options.RESTART,
        durable=not options.TRANSIENT,
        live_time=options.LIVE_TIME,
        wait_time=options.WAIT_TIME,
    )
    try:
        consumer.run()
    except KeyboardInterrupt:
        consumer.stop()
