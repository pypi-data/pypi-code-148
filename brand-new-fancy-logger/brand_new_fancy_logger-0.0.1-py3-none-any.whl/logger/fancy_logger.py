import logging
import sys

class CustomFormatter(logging.Formatter):

    grey = "\x1b[37;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = '%(asctime)s: %(levelname)s |  %(message)s  (%(filename)s:%(lineno)d)'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: format,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt,
                            datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class FileFormatter(CustomFormatter):

    format = '%(asctime)s: %(levelname)s |  %(message)s  (%(filename)s:%(lineno)d)'

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt,
                                      datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def flogger(logger_name: str, log_level: str, logpath: str ) -> logging.Logger:
    """
    your most beloved fancy logger. It's colorful and shiny!
    :param logger_name: give a name for your child!
    :param log_level: degrees of initiation - decide how much magic you want to see!
    :return: the best logger instance
    """
    log = logging.getLogger(logger_name)
    log.setLevel(log_level)

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setLevel(log_level)
    sh.setFormatter(CustomFormatter())
    log.addHandler(sh)

    fh = logging.FileHandler(logpath)
    fh.setFormatter(FileFormatter())
    log.addHandler(fh)

    return log

