"""
Some date routines.

On ISO 8601 date time see:

* `Date and Time Formats <https://www.w3.org/TR/NOTE-datetime>`_.

* `ISO date format <https://www.techtarget.com/whatis/definition/ISO-date-format>`_.

* `How to translate UTC to your time <https://earthsky.org/astronomy-essentials/universal-time/>`_.

Functions in this module handle, or rather assume, local time only. They haven't yet 
taken UTC into account. That is, date time output is in the format ``YYYY-MM-DD["T"HH:MM:SS]`` 
only.

For usage examples, see ``./tests/test_date_funcs.py``.
"""

from functools import singledispatch
from datetime import datetime

@singledispatch
def australian_date_to_iso_datetime(date_time_data, time=True):
    """Convert Australian date to ISO 8601 date and time format.
    
    This is an overloaded function.

    Australian date is in string format: ``D/M/YYYY HH:MM:SS [AM|PM]``, ``DD/MM/YYYY``, 
    etc. I.e., date and month can be either a single character without a leading 0, or 
    a two characters consist of a leading 0 and a non-0 digit.

    If the input string has the time component, it must be a 12-hour time, and must be 
    in the format: ``HH:MM:SS [AM|PM]``. E.g., ``01:23:34 PM``.
    
    1. Overload version 1:

    :param dict params: a dictionary contains two (2) input Australian date strings. 
        The dictionary keys are ``startDate`` and ``endDate``.

    :return: a tuple of two (2) strings in the format ``YYYY-MM-DD["T"HH:MM:SS]``, which 
        is the ISO version of ``startDate`` and ``endDate``.
    :rtype: tuple.

    2. Overload version 2:

    :param str date_str: the input Australian date string.

    :return: a string in the format ``YYYY-MM-DD["T"HH:MM:SS]``, which is the ISO version 
        of ``date_str``.
    :rtype: str.

    Finally, the common parameter:

    :param bool time: whether to include the time component in the output value.

    1. Overload version 1, usage example::

        d1, d2 = australian_date_to_iso_datetime({'startDate': '29/1/2022',
            'endDate': '1/12/2022'}, False)
    
        assert d1 == '2022-01-29'
        assert d2 == '2022-12-01'

    2. Overload version 2, usage example::

        date_str = australian_date_to_iso_datetime('29/1/2022', False)
       
        assert date_str == '2022-01-29'
	"""

    raise NotImplementedError

def __get_format_strings(time=True) -> tuple:    
    in_format = "%d/%m/%Y %I:%M:%S %p" if (time == True) else "%d/%m/%Y"
    out_format = "%Y-%m-%dT%H:%M:%S" if (time == True) else "%Y-%m-%d"

    return in_format, out_format

@australian_date_to_iso_datetime.register
def _(params: dict, time=True) -> tuple:
    """Converts input date strings to 'YYYY-MM-DD["T"HH:MM:SS]' date strings.
    """
    
    start_date = params["startDate"]
    end_date = params["endDate"]
    
    in_format, out_format = __get_format_strings(time)

    return (datetime.strptime(start_date, in_format).strftime(out_format),
        datetime.strptime(end_date, in_format).strftime(out_format))

@australian_date_to_iso_datetime.register
def _(date_str: str, time=True) -> str:
	"""Converts an input date string to 'YYYY-MM-DD["T"HH:MM:SS]' date string.
	"""

	in_format, out_format = __get_format_strings(time)

	return (datetime.strptime(date_str, in_format).strftime(out_format))