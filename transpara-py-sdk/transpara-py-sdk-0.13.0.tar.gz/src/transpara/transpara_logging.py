import logging
from logging import Logger
from transpara.logging_config import TRANSPARA_DEBUG_LEVEL, TRANSPARA_ERROR_LEVEL, CRITICAL_LEVEL, FATAL_LEVEL, ERROR_LEVEL, WARN_LEVEL, WARNING_LEVEL, INFO_LEVEL, DEBUG_LEVEL
from transpara.logging_config import RED, RESET_COLOR, BOLD_RED, BLUE, GREY, YELLOW
from transpara import logging_config

class TransparaLogger(Logger):
    
    def terror(self, msg):
        self.log(TRANSPARA_ERROR_LEVEL, msg)

    def tdebug(self, msg):
        self.log(TRANSPARA_DEBUG_LEVEL, msg)

#Monkeypatching the class as I don't want to lose information by calling the logger from an interim function
Logger.terror = TransparaLogger.terror
Logger.tdebug = TransparaLogger.tdebug

def get_logger(logger_name) -> TransparaLogger:
    return logging.getLogger(logger_name)

def set_log_level(level:int):
    logging.root.setLevel(level)

"""
Sets verbose exception stacks
"""
def set_global_verbose(val:bool):
    logging_config.GLOBAL_VERBOSE = val

def set_default_format(fmt:str):
    logging_config.default_format = fmt
    logging_config.stream_handler.setFormatter(logging_config.TransparaCustomLogFormatter())

def set_tdebug_format(fmt:str):
    logging_config.debug_handler_format = fmt
    logging_config.stream_handler.setFormatter(logging_config.TransparaCustomLogFormatter())

def set_terror_format(fmt:str):
    logging_config.error_handler_format = fmt 
    logging_config.stream_handler.setFormatter(logging_config.TransparaCustomLogFormatter())

