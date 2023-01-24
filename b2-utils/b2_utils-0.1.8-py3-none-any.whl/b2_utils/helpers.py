import random as _random

__all__ = [
    "random_hex_color",
    "get_nested_attr",
]


def random_hex_color(min_color=0x000000, max_color=0xFFFFFF) -> str:
    """Returns a random hexadecimal color in range [min_color, max_color], including
    both end points.

    Parameters
    ---------
    min_color : int
        Minimum value for color (default 0x000000)
    max_color : int
        Maximum value for color (default 0xFFFFFF)

    Returns
    -------
    str
        A random color "#XXXXXX" that is between min_color and max_color values.
    """

    return "#%06x".upper() % _random.randint(min_color, max_color)


def get_nested_attr(obj: any, path: str, raise_exception=False, default=None):
    """Gets nested object attributes, raising exceptions only when specified.

    Parameters
    ---------
    obj : any
        The object which attributes will be obtained
    path : str
        Attribute path separated with dots ('.') as usual
    raise_exception : bool = False
        If this value sets to True, an exception will be raised if an attribute cannot
        be obtained, even if default value is specified
    default : any = None
        A default value that's returned if the attribute can't be obtained. This
        parameter is ignored if raise_exception=True

    Returns
    -------
    any
        Attribute value or default value specified if any error occours while trying
        to get object attribute
    """

    for path_attr in path.split("."):
        if raise_exception:
            obj = getattr(obj, path_attr)
        else:
            obj = getattr(obj, path_attr, default)

    return obj
