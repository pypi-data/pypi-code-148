import logging
from typing import Dict, Any


def log_exception(source: str, exception: Exception):
    """
    To log exception to console
    usage: log_exception(MyClass, exception_object)
    
    :param source: 
    :param exception: 
    :return: 
    """
    logger = logging.getLogger(source)
    logger.exception(exception)


def log_debug(source: str, data: Any):
    logger = logging.getLogger(source)
    logger.info(msg=data)


def log_error(source: str, data: Any):
    logger = logging.getLogger(source)
    logger.error(msg=data)


def log_warning(source: str, data: Any):
    logger = logging.getLogger(source)
    logger.warning(msg=data)


def localize(data_dict: Dict, lang: str) -> str:
    _lang = lang.lower()
    if _lang in data_dict:
        return data_dict[_lang]
    first_lang = list(data_dict.keys())[0]
    log_warning("localize",
                f"Lang: {_lang} not found in ${data_dict}, "
                f"using {first_lang} instead")
    return data_dict[first_lang]
