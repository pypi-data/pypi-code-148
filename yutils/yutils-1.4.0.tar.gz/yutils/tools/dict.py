#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

LONG_VALUE_LIMIT = 120
LONG_VALUE_FILLER = '<Long {type} object with repr length {length}>'


def prioritize_dicts(*dicts):
    """
    Creates a new dict, prioritizing a more previous dict's keys/values from a later dict's keys/values.
    All of the first dict's keys/values will be present in the return dict.
    The other dicts' keys/values will be present only if no previous dictionaries had the same key.

    :param dicts: any number of dictionaries to prioritize between.
    :type dicts: dicts

    :return: A final dict
    :rtype: dict
    """
    final_dict = {}
    for dct in dicts:
        for key, value in dct.items():
            if key not in final_dict:
                final_dict[key] = value
    return final_dict


def repr_dict(dictionary, long_value_limit=LONG_VALUE_LIMIT, long_value_filler=LONG_VALUE_FILLER):
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
    string = ""
    indent_len = max([len(str(key)) for key in dictionary.keys()]) + 2
    for key, value in dictionary.items():
        repr_value = repr(value)
        if len(repr_value) > long_value_limit:
            repr_value = long_value_filler.format(type=type(value).__name__,
                                                  length=len(repr_value))
        spaces = ' ' * (indent_len - len(str(key)))
        string += f'{key}:{spaces}{repr_value}\n'
    return string[:-1]
