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

BASE_FLAGS = {"y", "M", "w", "d", "h", "m", "S", "s", "u", "z"}
PLURAL_FLAGS = {"p", "P", "ep", "eP", "Ep", "EP"}
MICROSECONDS_IN_MILLISECOND = 1_000
MICROSECONDS_IN_SECOND = 1_000_000
MICROSECONDS_IN_MINUTE = MICROSECONDS_IN_SECOND * 60
MICROSECONDS_IN_HOUR = MICROSECONDS_IN_MINUTE * 60
MICROSECONDS_IN_DAY = MICROSECONDS_IN_HOUR * 24
MICROSECONDS_IN_WEEK = MICROSECONDS_IN_DAY * 7
MICROSECONDS_IN_MONTH = MICROSECONDS_IN_DAY * 30
MICROSECONDS_IN_YEAR = MICROSECONDS_IN_MONTH * 12
MAP = {
    "y": MICROSECONDS_IN_YEAR,
    "M": MICROSECONDS_IN_MONTH,
    "w": MICROSECONDS_IN_WEEK,
    "d": MICROSECONDS_IN_DAY,
    "h": MICROSECONDS_IN_HOUR,
    "m": MICROSECONDS_IN_MINUTE,
    "S": MICROSECONDS_IN_SECOND,
    "s": MICROSECONDS_IN_MILLISECOND,
    "u": 1,
}
