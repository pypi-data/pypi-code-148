import logging

DEBUG = "DEBUG"
INFO = "INFO"
ERROR = "ERROR"
FATAL = "FATAL"
LOG_FORMATTING = '{"datetime": "%(asctime)s", "level_name": "%(levelname)s", "message": "%(message)s"}'


LOG_TYPE = {
    DEBUG: logging.DEBUG,
    INFO: logging.INFO,
    ERROR: logging.ERROR,
    FATAL: logging.FATAL,
}
