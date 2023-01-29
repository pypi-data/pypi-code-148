import logging
from typing import Iterable, Optional, Union


def getLogger(
    name: Optional[str] = None,
    *,
    level: Union[str, int, None] = None,
    handlers: Union[Iterable[logging.Handler], logging.Handler, None] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    if isinstance(handlers, logging.Handler):
        logger.addHandler(handlers)
    elif isinstance(handlers, Iterable):
        for hdlr in handlers:
            logger.addHandler(hdlr)
    return logger
