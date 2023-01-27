import logging
from environs import Env
from resources.custom_logger_formatter import CustomLoggerFormatter


def setup_logger(
    name: str,
    level: int = logging.DEBUG,
    Formatter: logging.Formatter = CustomLoggerFormatter,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(Formatter())

    logger.addHandler(ch)

    return logger


def get_env(props: any) -> str:
    env = Env()
    env.read_env()

    return env.str(props)
