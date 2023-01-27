import inspect
import logging
import os
from logging.handlers import RotatingFileHandler

_log = None


def configure(app_id: str, log_level: str = "DEBUG", log_fmt: str = "%(asctime)s %(levelname)s: %(message)s") -> None:
    global _log

    caller = inspect.stack()
    parent_path = os.path.dirname(caller[1].filename)

    log_file: str = f"{app_id}.log"
    log_path = os.path.join(parent_path, 'logs')
    log_file = os.path.join(log_path, log_file)
    log_backupcount: int = 50
    log_maxbytes: int = 10000000  # 10MB

    os.makedirs(log_path, exist_ok=True)

    file_handler = RotatingFileHandler(filename=log_file, maxBytes=log_maxbytes,
                                       backupCount=log_backupcount)
    file_handler.setFormatter(logging.Formatter(log_fmt))
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(logging.Formatter(log_fmt))
    _log = logging.getLogger(__name__)
    _log.addHandler(file_handler)
    _log.addHandler(stream_hander)
    _log.setLevel(log_level)


def i(v):
    _log.info(v)


def d(v):
    _log.debug(v)


def e(ex: Exception):
    _log.exception(ex)
