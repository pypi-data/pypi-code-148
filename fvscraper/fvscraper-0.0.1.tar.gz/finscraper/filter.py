from typing import Union
from .constants import FILTERS


def filter_exists(filter: str) -> bool:
    """Checks if a filter name exists

    Args:
        filter (str): filter name

    Returns:
        bool: whether or not the filter exists
    """
    return filter.lower() in list(FILTERS.keys())


def is_filter_value_allowed(filter: str, value: str) -> bool:
    """Checks if the value supplied exists for a filter

    Args:
        filter (str): filter name
        value (str): value/parameter of the filter

    Returns:
        bool: whether or not the value is allowed for the filter
    """
    if filter_exists(filter.lower()):
        return value.lower() in FILTERS[filter.lower()]["values"]

    else:
        raise ValueError(f"filter ({filter}) does not exist")


def prefixer(filter: str, value: str) -> str:
    """Prefixes the finviz code with the value to form part of the query string

    Args:
        filter (str): filter name
        value (str): value/parameter of the filter

    Returns:
        Union[str, None]: _description_
    """
    if filter_exists(filter.lower()) and is_filter_value_allowed(filter.lower(), value):
        return FILTERS[filter.lower()]["short"] + value.lower()
    
    else:
        raise ValueError(f"wrong combination of filter ({filter}) and value {value}")
