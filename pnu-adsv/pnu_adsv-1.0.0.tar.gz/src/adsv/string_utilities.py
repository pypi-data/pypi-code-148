#!/usr/bin/env python3
""" adsv - Analyze delimiter-separated values files
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import dateutil.parser


####################################################################################################
def get_string_type_and_value(string):
    """ Return the type and value of the string parameter's content """
    # int? Regular expression: [-+]?[0-9]+
    try:
        value = int(string)
        return "int", value
    except ValueError:
        pass

    # float? (with point decimal separator)
    # Regular expression: [-+]?([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?
    try:
        value = float(string)
        return "float", value
    except ValueError:
        pass

    # float? (with comma decimal separator)
    # Regular expression: [-+]?([0-9]*,[0-9]+|[0-9]+,[0-9]*)([eE][-+]?[0-9]+)?
    try:
        value = float(string.replace(".", ","))
        return "float", value
    except ValueError:
        pass

    # complex? (Python's format)
    # Regular expression: [-+]?([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)[-+]([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)j
    try:
        value = complex(string)
        return "complex", value
    except ValueError:
        pass

    # datetime?
    try:
        value = dateutil.parser.parse(string)
        return "datetime", value
    except dateutil.parser._parser.ParserError:
        pass

    # str!
    return "str", string
