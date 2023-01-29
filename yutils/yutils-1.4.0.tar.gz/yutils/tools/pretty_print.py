#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.tools.list import repr_list
from yutils.tools.dict import repr_dict, LONG_VALUE_LIMIT, LONG_VALUE_FILLER


def pprint_dict(dictionary, long_value_limit=LONG_VALUE_LIMIT, long_value_filler=LONG_VALUE_FILLER):
    """
    Prints a dict in a very pretty way!

    :param dictionary: your dict to print
    :type dictionary: dict
    :param long_value_limit: when a dict value exceeds this limit, it won't be printed
                             Default: 120
    :type long_value_limit: int
    :param long_value_filler: A filler to print instead of a long value, must have {type} and {length} fields!
                              Default: '<Long {type} object with repr length {length}>'
    :type long_value_filler: str
    :return: None
    """
    print(repr_dict(dictionary, long_value_limit, long_value_filler))


def pprint_list(list_to_print):
    """
    Prints a list in an easy, short way.

    :param list_to_print: the list you wish to print
    :type list_to_print: list
    :return: None
    """
    print(repr_list(list_to_print))
