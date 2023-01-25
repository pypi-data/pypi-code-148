"""Some custom conversion functions.

For usage examples, see ``./tests/test_conversions.py``.
"""
from typing import Union

def str_to_bool(str_val: str, exception_msg=None) -> Union[bool, None]:
    """Convert a string to Boolean.
	
    :Reference: 
    
        * `Converting from a string to boolean in Python \
            <https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python>`_

    If str_val can be converted to Boolean, then return a Boolean value. Otherwise, 
    return None if exception_msg is None; raise an exception otherwise.
	
    The behaviour of this function is different to the standard function 
    `distutils.util.strtobool(val) <https://docs.python.org/3/distutils/apiref.html?highlight=strtobool#distutils.util.strtobool>`_.

    :param str str_val: a string to be converted to Boolean.
    :param str exception_msg: the exception message to be raised if str_val can't be converted to Boolean.

    :return: a Boolean if str_val can be converted. None if can't be converted and exception_msg is None.
    :rtype: Bool or None.

    :raises Exception: if str_val can not be converted and exception_msg is not None.
    """
	
    res = None

    if str_val.lower() in ['true', '1', 't', 'yes', 'y', 'on']: 
        res = True
    elif str_val.lower() in ['false', '0', 'f', 'no', 'n', 'off']: 
        res = False

    # Succeeds.
    if (res != None): return res

    # Not succeeded. No exception required. Returns None.
    if (exception_msg == None): return res

    # Not succeeded. Exception required: raise exception.
    if (res == None): raise Exception(exception_msg)
	
def is_integer(value: Union[int, str]) -> bool:
    """
    Check whether the value of a variable is an integer or can be converted to an integer.

    :Reference: 
    
        * `Checking whether a variable is an integer or not \
            <https://stackoverflow.com/questions/3501382/checking-whether-a-variable-is-an-integer-or-not>`_

    :param [int, str] value: value to be checked.

    :return: True if value is an integer or can be converted to an integer. False otherwise.
    :rtype: Bool.
    """	
    if (isinstance(value, int)): return True
    if (isinstance(value, str)):
        if value.isnumeric(): return True
    return False