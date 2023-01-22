"""MIT License

Copyright (c) 2023-present Tanner B. Corcoran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from typing import Union
from . import exceptions
from . import formatter
from . import constants
from . import models
from . import types
from . import utils
import datetime
import plogging
import logging
import typing
import re


class Countdown:
    """The main class used to format and parse countdown strings.

    """
    _log = plogging.setup_new("Countdown", level=logging.INFO, package=__name__)
    def __init__(self, fmt: types.SupportsBracketFormat, remove_empty: bool = True,
                 max_value: int = None, strip_output: bool = True,
                 **defaults: Union[typing.Callable[[models.TimeValue], typing.Any], typing.Any]
                 ) -> None:
        """
        Arguments
        ---------
        fmt : str
            The bracket-style format string.
        remove_empty : bool, default=True
            If `True`, any flags that equal 0 will be removed from the result when formatted.
        max_value : int, default=None
            If given a value, the maximum number for each flag will be the given value.
        strip_output : bool, default=True
            If `True`, `str.strip()` will be run on the output before being returned.
        **defaults : Any
            Default values for the fields in `fmt`.
        
        """
        Countdown._log.debug(f"Updating format string: '{fmt}'")
        self.__ofmt = fmt
        self.__flags, self.__fmt = formatter.update_fmt(fmt)
        self._remove_empty = remove_empty
        self._max_value = max_value
        self._strip_output = strip_output
        self._defaults = defaults
    
    @property
    def flags(self) -> formatter.Flags:
        """The `Flags` object that has been constructed from the given format string.
        
        """
        return self.__flags
    
    @property
    def orig_fmt(self) -> str:
        """The original format string.
        
        """
        return self.__ofmt
    
    @property
    def fmt(self) -> str:
        """The updated format string.
        
        """
        return self.__fmt
    
    @utils.StaticProperty
    def default() -> "Countdown":
        """Create and return the default `Countdown` instance.
        
        """
        Countdown._log.debug("Creating default formatter")
        return Countdown("{y}{yd}{M}{Md}{w}{wd}{d}{dd}{h}{hd}{m}{md}{S}{Sd}", yd="y ", Md="mo ",
                         wd="w ", dd="d ", hd="h ", md="m ", Sd="s")

    def parse(self, parsable: str) -> models.TimeValue:
        """Attempt to parse `parsable` string into a new `TimeValue` object.
        
        """
        def get_int(__str: str) -> int:
            if __str == "+":
                return 1
            if __str == "-":
                return -1
            return int(__str)
        
        # prepare parsing info
        parse_info = [(flag.name, flag.get_parse_info(self._defaults)) if flag.name != "z" else
                      (flag.name, flag.get_parse_info(self._defaults, "(-|\\+)"))
                      for flag in self.__flags]
        parse_info.sort(key=lambda a: a[1][1], reverse=True)
        tval = models.TimeValue()

        # start searching through the parsable str
        for flag_name, (pat, _) in parse_info:
            matches = list(re.finditer(pat, parsable))
            num_matches = len(matches)
            if num_matches == 0:
                continue
            if num_matches > 1:
                m1_val = matches[0].group(0)
                if not all(m.group(0) == m1_val for m in matches[1:]):
                    msg = "', '".join(m.group(0) for m in matches)
                    raise exceptions.ParseError(f"Multiple matches found for flag '{flag_name}': "
                                                f"'{msg}'")
            tval.set(flag_name, get_int(matches[0].group(1)))

            # we remove the match in the string afterwards so later
            # matches have a better chance of succeeding
            parsable = re.sub(pat, "", parsable)
        
        return tval


    def format(self, microseconds: Union[int, float], *, ignore: bool = False) -> str:
        """The core method for formatting the format string with the given microseconds. All other
        format methods in `Countdown` convert to microseconds, then call this method.
        
        """
        Countdown._log.debug(f"Formatting format string from microseconds: {microseconds}")
        z_flag = 1 if microseconds >= 0 else -1
        remaining = abs(int(microseconds))

        fmt_kwargs = {"z": "+" if z_flag == 1 else "-"}
        tval = models.TimeValue(z=z_flag)

        # these will be run later
        funcs: dict[str, typing.Callable[[models.TimeValue], typing.Any]] = dict()

        # if the flag name is present in our Flags instance, then convert; otherwise, move on
        for flag_name, div in constants.MAP.items():
            flag: formatter.Flag = self.__flags.get(flag_name, None)
            if not flag:
                continue
            value, remaining = divmod(remaining, div)
            if self._max_value and value > self._max_value:
                remaining += (value - self._max_value) * div
                value = self._max_value

            tval.set(flag_name, value)

            if value == 0 and self._remove_empty:
                fmt_kwargs.update(flag.get_empty_kwargs())
                continue

            fmt_kwargs[flag_name] = value

            extra_kwargs, extra_funcs = flag.get_extras(self._defaults)
            fmt_kwargs.update(extra_kwargs)
            funcs.update(extra_funcs)

            if value in [1, -1]: # 1 and -1 are singular
                fmt_kwargs.update(flag.get_empty_plurals())
            else:
                fmt_kwargs.update(flag.get_plurals())

        for flag_name, func in funcs.items():
            if ignore:
                try:
                    fmt_kwargs[flag_name] = func(tval)
                except Exception:
                    fmt_kwargs[flag_name] = str(func)
            else:
                fmt_kwargs[flag_name] = func(tval)

        formatted = self.__fmt.format(**fmt_kwargs)
        if self._strip_output:
            return formatted.strip()
        return formatted

    def format_time(self, weeks: Union[int, float] = None, days: Union[int, float] = None,
                    hours: Union[int, float] = None, minutes: Union[int, float] = None,
                    seconds: Union[int, float] = None, milliseconds: Union[int, float] = None,
                    microseconds: Union[int, float] = None) -> str:
        """Similar to `.format_timedelta` but does not require you to input a timedelta instance.
        
        """
        return self.format_timedelta(datetime.timedelta(weeks=weeks or 0, days=days or 0,
                                                        hours=hours or 0, minutes=minutes or 0,
                                                        seconds=seconds or 0,
                                                        milliseconds=milliseconds or 0,
                                                        microseconds=microseconds or 0))

    def format_microseconds(self, microseconds: Union[int, float]) -> str:
        """An alias for `.format`.
        
        """
    format_microseconds = format

    def format_milliseconds(self, milliseconds: Union[int, float]) -> str:
        """Format the format string given a number of seconds.
        
        """
        return self.format(milliseconds * constants.MICROSECONDS_IN_MILLISECOND)

    def format_seconds(self, seconds: Union[int, float]) -> str:
        """Format the format string given a number of seconds.
        
        """
        return self.format(seconds * constants.MICROSECONDS_IN_SECOND)

    def format_minutes(self, minutes: Union[int, float]) -> str:
        """Format the format string given a number of minutes.
        
        """
        return self.format(minutes * constants.MICROSECONDS_IN_MINUTE)

    def format_hours(self, hours: Union[int, float]) -> str:
        """Format the format string given a number of hours.
        
        """
        return self.format(hours * constants.MICROSECONDS_IN_HOUR)

    def format_days(self, days: Union[int, float]) -> str:
        """Format the format string given a number of days.
        
        """
        return self.format(days * constants.MICROSECONDS_IN_DAY)

    def format_weeks(self, weeks: Union[int, float]) -> str:
        """Format the format string given a number of weeks.
        
        """
        return self.format(weeks * constants.MICROSECONDS_IN_WEEK)
    
    def format_timedelta(self, td: datetime.timedelta) -> str:
        """Format the format string given a datetime.timedelta instance.
        
        """
        return self.format(td.total_seconds() * constants.MICROSECONDS_IN_SECOND)

    def format_datetime(self, dt: datetime.datetime, dt2: datetime.datetime = None) -> str:
        """Format the format string given a datetime object and an optional second datetime
        object. If the second datetime object is not provided, a new one will be created with the
        current time. The timedelta is acquired from `dt2 - dt`.
        
        """
        if dt2 is None:
            dt2 = datetime.datetime.now(tz=dt.tzinfo)
        td = dt2 - dt
        return self.format_timedelta(td)

