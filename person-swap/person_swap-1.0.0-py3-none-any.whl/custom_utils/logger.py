import logging


def get_logger(name):
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name)
