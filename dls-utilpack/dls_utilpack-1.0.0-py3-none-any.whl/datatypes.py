"""
Validate strings according to expected data types.
The allowed data types are denoted as string constants
so these can be specified in string-based configuration such as yaml.

At time of writing, only integer datatypes are handled.
It is intended to add more such as float, filename, dict, etc.
"""

from typing import Any


class Datatypes:
    """
    Class with symbolic constants denoting the allowed data types.
    """

    INTEGER = "integer"  #:


# --------------------------------------------------------------------------------
def __verify_integer(name: str, value: Any) -> int:
    """
    Return the given value converted to an integer.

    Args:
        name (str): name for use in the possible exception
        value (Any): value expected to be convertable into an integer

    Raises:
        ValueError: if the value cannot be converted

    Returns:
        int: integer value from the conversion
    """

    try:
        if isinstance(value, float):
            raise ValueError("value is a builtin float")
        if isinstance(value, bool):
            raise ValueError("value is a builtin bool")

        integer_value = int(value)
    except Exception:
        raise ValueError(
            f'unable to verify {name} value "{value}" as integer',
        )

    return integer_value


# --------------------------------------------------------------------------------
def verify(name: str, value: Any, datatype: str) -> Any:
    """
    Return the given value converted according to datatype.

    Args:
        name (str): name for use in the possible exception
        value (Any): value expected to be convertable into datatype
        datatype (str): symbolic constant of the datatype

    Raises:
        ValueError: if the value cannot be converted
        RuntimeError: if the datatype is invalid

    Returns:
        Any: value from the conversion
    """

    if datatype == Datatypes.INTEGER:
        return __verify_integer(name, value)
    else:
        raise RuntimeError(f"cannot verify datatype {datatype}")
