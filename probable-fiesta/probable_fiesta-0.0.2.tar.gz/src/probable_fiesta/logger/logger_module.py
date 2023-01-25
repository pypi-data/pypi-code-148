from .builder.logger_abstract_machine import LoggerMachine
from ..config.variables import LoggerDef as ld

def get_logger(type=None, app=None, name=None, level=None, fmt=None, directory=None):
    if type is None:
        type = ld.TYPE
    if directory is None:
        directory = ld.DIRECTORY
    lM =  LoggerMachine()
    logger = lM.make_logger(type, app, name, level, fmt, directory)
    return logger.get_logger()
