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
from . import constants
from . import types
import plogging
import logging
import typing


class TimeValue:
    """Stores a time value partitioned into weeks, days, hours, minutes, seconds, milliseconds,
    and/or microseconds.
    
    """
    _log = plogging.setup_new("TimeValue", level=logging.INFO, package=__name__)
    def __init__(self, z: typing.Literal[1, -1] = 1, y: Union[int, float] = None,
                 M: Union[int, float] = None, w: Union[int, float] = None,
                 d: Union[int, float] = None, h: Union[int, float] = None,
                 m: Union[int, float] = None, S: Union[int, float] = None,
                 s: Union[int, float] = None, u: Union[int, float] = None) -> None:
        self.z = z
        self.y = y
        self.M = M
        self.w = w
        self.d = d
        self.h = h
        self.m = m
        self.S = S
        self.s = s
        self.u = u

    @typing.overload
    def get(self, name: str, /) -> Union[int, float, None]: ...
    @typing.overload
    def get(self, name: str, default: types.T, /) -> Union[int, float, None, types.T]: ...
    def get(self, name: str, default = types.MISSING, /):
        """Get the stored time value given a valid flag name and optional default.
        
        """
        if default is types.MISSING:
            TimeValue._log.debug(f"Acquiring value from flag name: '{name}'")
            if name not in constants.BASE_FLAGS:
                raise ValueError(f"Invalid flag name: '{name}'")
            return getattr(self, name)
        
        TimeValue._log.debug(f"Acquiring value from flag name: '{name}'; default={default}")
        if name not in constants.BASE_FLAGS:
            return default
        return getattr(self, name)

    def set(self, name: str, value: Union[int, float, None], /) -> None:
        """Set the given flag specified by `name` to `value`.
        
        """
        if name not in constants.BASE_FLAGS:
            raise ValueError(f"Invalid flag name: '{name}'")
        setattr(self, name, value)

    @property
    def sign(self) -> typing.Literal[1, -1]:
        return self.z
    
    @property
    def years(self) -> Union[int, float, None]:
        return self.y
    
    @property
    def months(self) -> Union[int, float, None]:
        return self.M

    @property
    def weeks(self) -> Union[int, float, None]:
        return self.w
    
    @property
    def days(self) -> Union[int, float, None]:
        return self.d
    
    @property
    def hours(self) -> Union[int, float, None]:
        return self.h
    
    @property
    def minutes(self) -> Union[int, float, None]:
        return self.m
    
    @property
    def seconds(self) -> Union[int, float, None]:
        return self.S
    
    @property
    def milliseconds(self) -> Union[int, float, None]:
        return self.s
    
    @property
    def microseconds(self) -> Union[int, float, None]:
        return self.u

    def total_microseconds(self) -> int:
        return sum(map(lambda k, v: (self.get(k) or 0) * v, constants.MAP.keys(), constants.MAP.values())) * self.z

    def total_milliseconds(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_MILLISECOND

    def total_seconds(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_SECOND

    def total_minutes(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_MINUTE

    def total_hours(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_HOUR

    def total_days(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_DAY

    def total_weeks(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_WEEK
    
    def total_months(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_MONTH
    
    def total_years(self) -> float:
        return self.total_microseconds() / constants.MICROSECONDS_IN_YEAR
