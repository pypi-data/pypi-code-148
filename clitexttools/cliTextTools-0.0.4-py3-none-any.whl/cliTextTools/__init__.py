import os
import time
import sys
import random

TIMING_RANGE_LOW = 1
TIMING_RANGE_HIGH = 3
TIMING_DIVISOR = 10
SPACE_TIMING = 0.8

INT_TYPE = "int"
STR_TYPE = "str"
BOOL_TYPE = "bool"
FLOAT_TYPE = "flt"

PLTFRM = sys.platform


def typing_print(message: str, *args, **kwargs):
    """
    Description:
        Simulates the typing of a keyboard with a given message
    :param message: The message you wish to simulate a keyboard with
    :return: None
    """
    for char in message:
        if char in (" ", "_", "-", "\n"):
            time.sleep(SPACE_TIMING)
        else:
            sleep = random.randrange(TIMING_RANGE_LOW, TIMING_RANGE_HIGH) / TIMING_DIVISOR
            time.sleep(sleep)
        print(char, end="", flush=True, *args, **kwargs)
    print("\n", end="", flush=True, *args, **kwargs)


def get_user_input(message: str, expected_type: str, can_cancel: bool = True, print_func=print, allow_newlines: bool = True, *args, **kwargs):
    """
    Description:
        get user input and returns the expected datatype
    :param message: the message to tell the user what to type
    :param expected_type: a string consisting of the type of data the user needs to enter
    :param can_cancel: a bool that decides if the user can cancel
    :param print_func: the function to which the messages be printed
    :return: The data in the type equal to expected_type or None if the user cancels
    """
    print_func(message, *args, **kwargs)
    data = input(">>> ")
    if data.lower() in ("cancel", "", "cancel."):
        if can_cancel:
            return None
        print_func("invalid entry. try again")
        return get_user_input(message, expected_type, can_cancel, print_func)
    if expected_type == INT_TYPE:
        try:
            data = int(data)
        except ValueError:
            print_func("invalid entry. try again")
            return get_user_input(message, expected_type, can_cancel, print_func)
        return data
    elif expected_type == STR_TYPE:
        if allow_newlines:
            data = _parse_string_mods(data)
        return data
    elif expected_type == BOOL_TYPE:
        if data.lower() in ("n", "no", "nope", "0", "false", "nah"):
            return False
        if data.lower() in ("y", "yes", "yeah", "1", "true", "yup"):
            return True
        print_func("invalid entry. try again.")
        return get_user_input(message, expected_type, can_cancel, print_func)
    elif expected_type == FLOAT_TYPE:
        try:
            return convert_string_to_float(data)
        except ValueError:
            print_func("invalid entry. try again")
            return get_user_input(message, expected_type, can_cancel, print_func)
    else:
        raise NotImplementedError


def convert_string_to_float(data: str):
    """
    Description:
        converts string to float
    Parameters:
        :param data: str: the data to convert
        :return: float: the converted output
    """
    base, fract = data.split(".")
    base = int(base)
    flen = len(fract)
    fract = int(fract)
    fract /= 10 ** flen
    return fract + base


def set_term_title(name: str):
    if PLTFRM in ("linux", "darwin"):
        sys.stdout.write(f"\x1b]2;{name}\x07")
    elif PLTFRM in ("win32", "cygwin"):
        os.system(f"title {name}")
    else:
        raise NotImplementedError


def _parse_string_mods(string: str):
    data = ""
    if len(string.split("\\t")) != 0:
        for i in string.split("\\n"):
            data = f"{data}\n{i}"
    if len(string.split("\\t")) != 0:
        for i in data.split("\\t"):
            data = f"{data}\t{i}"
    return data