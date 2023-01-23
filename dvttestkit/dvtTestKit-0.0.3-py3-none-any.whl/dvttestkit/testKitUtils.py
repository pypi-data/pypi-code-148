"""
    Minim Internal testing Software
    Utilities Package for TestKit
"""
import errno
import logging
import os
import re
import socket
import subprocess
import time
import platform
from datetime import datetime
from pathlib import Path
from typing import List

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Create utils specific fallback logger for Debugging debug mode
logger = logging.getLogger(__name__)
project = __name__
fileDate = datetime.now().strftime("%Y-%m-%d")
os.environ['ROOT_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def establishBroker():
    """
    Connect to the MQTT broker for logger mqttHandler stream
    :return:
    """
    _client = mqtt.Client()
    _client.connect(host=os.environ.get('AWSIP', 'localhost'),
                    port=int(os.environ.get('AWSPORT', 1884))
                    )
    return _client


def makeLogger(name: str = __name__, log_to_file: bool = False,
               log_level: str = 'DEBUG') -> logging.Logger:
    """
    Create the project wide logger.

    :param name: The name of the logger.
    :param log_to_file: Whether to log to a file.
    :param log_level: The log level to use (e.g. 'DEBUG', 'INFO').
    :return: A logger object.
    """
    name = name.replace(".", "/")
    _format = '%(asctime)s - %(module)s - %(message)s' if log_level == 'DEBUG' else '%(asctime)s - %(message)s'

    log = logging.getLogger(name)
    log.setLevel(log_level)

    if log_to_file:
        filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-TestKit.log"
        _log = ensure_exists(Path(os.environ['ROOT_DIR']).joinpath(f"data//{filename}"))
        file_handler = logging.FileHandler(_log)
        file_handler.setFormatter(logging.Formatter(_format))
        log.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_format))
    log.addHandler(stream_handler)

    my_handler = mqttHandler(topic=f'DVT/{name}')
    log.addHandler(my_handler)
    return log


def remove_file(files: List[str]) -> bool:
    """
    Removes old copies of files if they exist.

    :param files: The names of the files to remove.
    :return: `True` if all files were removed successfully, `False` otherwise.
    """
    success = True
    for f in files:
        try:
            os.remove(f)
            logger.debug(f'Removing previous copy of {f}..')
        except OSError:
            success = False
    return success


def linePrepender(file, line, depth: int = 0, mode: int = 0):
    """
    Prepends given line to given file at depth.
    :param file: Filepath to write too
    :param line: str to write
    :param depth: # of Lines to move away from mode
    :param mode: 0=Top,1=current,2=Bottom
    :return:
    """
    with open(file, 'r+') as _file:
        _file.seek(depth, mode)
        _file.write(line.rstrip('\r\n') + '\n' + _file.read())


def ensure_exists(path):
    """
    Accepts path to file, then creates the directory path if it does not exist
    :param path:
    :return:
    """
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path


class mqttHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a MQTT server to a topic.
    """

    def __init__(
            self,
            _hostName=os.environ.get('AWSIP', 'localhost'),
            topic=f'{project}/{os.environ.get(f"{project}_device")}/log',
            qos=1, retain=True,
            _port=int(os.environ.get('AWSPORT', 1884)),
            client_id='',
            keepalive=60,
            will=None,
            auth=None,
            tls=None,
            protocol=3,
            transport='tcp',
    ):
        logging.Handler.__init__(self)
        self.topic = topic
        self.qos = qos
        self.retain = retain
        self.hostname = _hostName
        self.port = _port
        self.client_id = client_id
        self.keepalive = keepalive
        self.will = will
        self.auth = auth
        self.tls = tls
        self.protocol = protocol
        self.transport = transport

    def emit(self, record):
        """
        Publish a single formatted logging record to a broker,
        then disconnect cleanly
        """
        msg = self.format(record)
        publish.single(
            self.topic,
            msg,
            self.qos,
            self.retain,
            hostname=self.hostname,
            port=self.port,
            client_id=self.client_id,
            keepalive=self.keepalive,
            will=self.will,
            auth=self.auth,
            tls=self.tls,
            protocol=self.protocol,
            transport=self.transport
        )


def post(topic: str, payload: str, retain: bool = False,
         _client=establishBroker()):
    """
    Post msg to MQTT broker
    :type _client: object
    :type retain: bool
    :param _client: Logging handler. By default, it is created by this module
    :param retain: Retain topic on broker
    :param topic: Project name
    :param payload: Sensor Data
    """
    topic = str(f'{project}/{topic}')
    payload = str(payload)
    try:
        _client.publish(topic=topic, payload=payload, qos=0, retain=retain)
    except ValueError:
        logger.warning(
            f"pub Failed because of wildcard: {str(topic)}=:={str(payload)}")
        logger.warning(f"Attempting fix...")
        try:
            tame_t = topic.replace("+", "_")
            tame_topic = tame_t.replace("#", "_")
            tame_p = payload.replace("+", "_")
            tame_payload = tame_p.replace("#", "_")
            _client.publish(topic=str(tame_topic), payload=str(tame_payload),
                            qos=1, retain=retain)
            logger.debug("Fix successful, Sending data...")
        except Exception as error:
            logger.warning(f"Fix Failed. Bug report sent.")
            _client.publish(f"{project}/error", str(error), qos=1, retain=True)


def run_command(command: str) -> str:
    """
    Run a command in the shell.

    :param command: The command to run.
    :type command: str
    :return: The output of the command.
    :rtype: str
    """
    process = subprocess.run(command, shell=True, capture_output=True,
                             text=True)
    return process.stdout


def get_ip() -> str:
    """
    Retrieve the IP address of the current machine.

    :return: A string containing the IP address of the current machine
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def ping_ip(ip_address="192.168.0.1") -> bool:
    """Pings the given IP address until it is successful.

   :param ip_address: The IP address to ping.
   :type ip_address: str
   :returns: bool

   .. note:: This function uses the `ping` command to ping the given IP address. It will continue to run
             the `ping` command until it is successful (i.e. the `ping` command returns a return code of 0)
    """
    # Determine the appropriate flag for the ping command based on the operating system
    if platform.system() == "Windows":
        ping_flag = "-n"
    else:
        ping_flag = "-c"

    while True:
        result = subprocess.run(["ping", ping_flag, "1", ip_address],
                                stdout=subprocess.PIPE)
        if result.returncode == 0:
            # Ping was successful
            return True
        else:
            logger.debug(f"Waiting for DUT to power on: {result.returncode}")
            time.sleep(4)


def parse_string(string: str, pattern: str) -> str:
    """Parse a string using the given regular expression pattern.

    :param string: The string to parse.
    :type string: str
    :param pattern: The regular expression pattern to use for parsing.
    :type pattern: str
    :return: The parsed string.
    :rtype: str
    """
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return "Not Found"


def parse_integer(string: str, pattern: str) -> int:
    """Parse an integer from a string using the given regular expression pattern.

    :param string: The string to parse.
    :type string: str
    :param pattern: The regular expression pattern to use for parsing.
    :type pattern: str
    :return: The parsed integer.
    :rtype: int
    """
    match = re.search(pattern, string)
    if match:
        return int(match.group(1))


def parse_status(string: str) -> int:
    """Parse an integer from a string using the regular expression pattern 'INTEGER: (\d+)'.

    :param string: The string to parse.
    :type string: str
    :return: The parsed integer.
    :rtype: int
    """
    return parse_integer(string, r'INTEGER: (\d+)')


if __name__ == '__main__':
    # get_slack_messages()
    # print(post_slack_message())
    post(topic="test", payload="message", retain=True)
    logger = makeLogger(__name__, True, 'DEBUG')
    logger.info("Info message")
    logger.debug("Debug  message")
    logger.warning("Warning message")
