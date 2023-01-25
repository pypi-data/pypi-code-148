import logging
import sys
from dataclasses import dataclass, field
from pprint import pformat
from typing import Callable, Any, List
from loguru import logger
from loguru._defaults import LOGURU_FORMAT


@dataclass
class LoggerConfig:

    startswith: List[str] = field(default_factory=list)
    endswith: List[str] = field(default_factory=list)
    contains: List[str] = field(default_factory=list)
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (
            self.startswith
            or self.endswith
            or self.contains
            or self.exclude
            or self.include
        )
    

    def __contains__(self, __name: str):
        result = False
        for base in self.startswith:
            if __name.startswith(base):
                result = True
                break
        else:
            for base in self.endswith:
                if __name.endswith(base):
                    result = True
                    break
            else:
                for base in self.contains:
                    if base in __name:
                        result = True
                        break
        if result:
            if __name in self.exclude:
                result = False
        elif __name in self.include:
            result = True
        return result


class InterceptHandler(logging.Handler):
    def __init___(self, record_callback: Callable[[logging.LogRecord], str]):
        super().__init__()
        self.record_callback = record_callback

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        message = self.record_callback(record)
        logger.opt(depth=depth, exception=record.exc_info).log(level, message)


def format_record(record: dict) -> str:

    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging(
    logger_config: LoggerConfig = LoggerConfig(
        startswith=[], endswith=[], contains=[], include=[], exclude=[]
    )
):

    if not logger_config.is_empty:
        system_loggers = [
            logging.getLogger(name) for name in logging.root.manager.loggerDict
        ]
        system_loggers_names = [sublogger.name for sublogger in system_loggers]
        system_loggers_names.sort()
        logged_modules = [
            sublogger for sublogger in system_loggers if sublogger.name in logger_config
        ]
        for sublogger in logged_modules:
            sublogger.handlers = []

        intercept_handler = InterceptHandler(level=logging.DEBUG)
        for logged_module in logged_modules:
            logging.getLogger(logged_module).handlers = [intercept_handler]

        logger.configure(
            handlers=[
                {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}
            ]
        )


def log(__level: int or str, __message: str, *args: Any, **kwargs: Any):
    logger.log(__level, __message, *args, **kwargs)


def info(__message: str, *args: Any, **kwargs: Any):
    logger.info(__message, *args, **kwargs)


def error(__message: str, *args: Any, **kwargs: Any):
    logger.error(__message, *args, **kwargs)


init_logging(
    logger_config=LoggerConfig(startswith=["sqlalchemy."], endswith=["transcribe"])
)
