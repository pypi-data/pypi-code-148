"""Configuration file for logging."""
import logging

from ..config.variables import LoggerDef as ld

# Catchall
if not ld.LEVEL:
    ld.LEVEL = logging.INFO
if not ld.NAME:
    ld.NAME = "main_log"
if not ld.FORMAT:
    ld.FORMAT = "simple"


def get_logger(log_name=ld.NAME):
    """Get a configured logger.
    :param log_name: Name of the logger
    """
    logger = logging.getLogger(log_name)
    return logger

# Create a simple logger in default directory "/Logger"
def set_logger(log_name=ld.NAME, log_level=ld.LEVEL, format=ld.FORMAT):
    """Create a simple logger in the default directory.
    :param log_name: Name of the logger and logger_name.log.
    :param log_level: logging.Debug, logging.Warning, etc.
    :param format: Formatter to use. See `set_formatter_format(option)`.
    :return: logger.
    """
    # Create Logger with name and level
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # Define a formatter for the Logger (Defaults to simple)
    formatter = set_formatter_format(format)

    # Set path of the logger using ROOT_DIR and log_name
    path = f"{ld.DIRECTORY}/{log_name}.log"
    print(f"Using {path} as the log file")

    # Set the and formatter and fileHandler
    fileh = logging.FileHandler(path, 'a')
    fileh.setFormatter(formatter)
    logger.addHandler(fileh)

    return logger  # Return Logger


def set_formatter_format(option='simple'):
    """Choose a formatter from the following or create your own.
    `simple` - Time LoggerName Level - Message
    `process` - Time moduleName -> processId lineNo Level - Message
    `function` - Time moduleName funcName -> lineNo Level - Message
    :param options: simple, process, function, custom.
    :return: formatter to be set with `setFormatter`.
    """
    # Check for valid input
    options = ['simple', 'process', 'function']
    if option not in options:
        print("Input error!")
        raise ValueError
    # Define a simple formatter
    if option == 'simple':
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Define a process formatter
    if option == 'process':
        return logging.Formatter(
            '%(asctime)s %(module)s -> %(process)d %(lineno)d %(levelname)s' +
            ' -  %(message)s')
    # Define a function formatter
    if option == 'function':
        return logging.Formatter(
            '%(asctime)s %(module)s %(funcName)s -> %(lineno)d %(levelname)s' +
            ' -  %(message)s')
