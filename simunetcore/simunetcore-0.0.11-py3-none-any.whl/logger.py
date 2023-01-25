import logging
import logging.config
import json
import os
from simunetcore import utils

instance = None

def prepare_logging(cfg_file="log.conf"):
    """
    Prepares the logging for simunet.

    Parameters
    ----------
    cfg_file : str, optional
        The log config file.
        Default="log.conf".

    See Also
    --------
    logging library : simunet uses logging for logging purposes.

    """
    
    if os.path.isfile(cfg_file):
        with open(cfg_file, "r") as f:
            cfg = json.load(f)
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig()
        
def debug(msg):
    """
    Writes a debug message.

    Parameters
    ----------
    msg : str
        The message to log.

    """
    
    if instance:
        instance.debug(msg)
    else:
        print("{} - {}".format(utils.current_time(), msg))
        
def info(msg):
    """
    Writes a info message.

    Parameters
    ----------
    msg : str
        The message to log.

    """
    
    if instance:
        instance.info(msg)
    else:
        print("{} - {}".format(utils.current_time(), msg))

def warning(msg):
    """
    Writes a warning message.

    Parameters
    ----------
    msg : str
        The message to log.

    """
    
    if instance:
        instance.warning(msg)
    else:
        print("{} - {}".format(utils.current_time(), msg))
    
def error(msg):
    """
    Writes an error message.

    Parameters
    ----------
    msg : str
        The message to log.

    """

    if instance:
        instance.error(msg)
    else:
        print("{} - {}".format(utils.current_time(), msg))

def exception(msg):
    """
    Writes an exception message.

    Parameters
    ----------
    msg : str
        The message to log.

    """

    if instance:
        instance.error(msg)
    else:
        print("{} - {}".format(utils.current_time(), msg))

def critical(msg):
    """
    Writes a critical message.

    Parameters
    ----------
    msg : str
        The message to log.

    """

    if instance:
        instance.error(msg)
    else:
        print("{} - {}".format(utils.current_time(), msg))
