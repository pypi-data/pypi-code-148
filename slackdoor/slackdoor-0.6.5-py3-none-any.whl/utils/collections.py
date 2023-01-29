from typing import Any, Callable, Iterable


def ensure_iterable(maybe_iterable: Any, desired_type: Callable[..., Iterable] | None = None) -> Iterable:
    """
    Make sure the passed-in arg is iterable.

    To ensure a specific type is returned, specify desired_type (default is a
    tuple if conversion needed and desired_type is unspecified)
    """
    if isiter(maybe_iterable):
        return maybe_iterable if desired_type is None else desired_type(maybe_iterable)

    if desired_type is None:
        desired_type = tuple

    return desired_type() if maybe_iterable is None else desired_type([maybe_iterable])


def isiter(obj: Any) -> bool:
    """
    Check if the object is an iterable, but not a string

    Parameters:
        obj (any): Object to check

    Returns (bool):
        True if the supplied object is an iterable, but not a string or bytes
    """
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))
