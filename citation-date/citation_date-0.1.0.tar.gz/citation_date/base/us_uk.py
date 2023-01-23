import re

from .day import day
from .month import month
from .year import year

separator = r"[,\.\s]*"

uk = rf"""
(
    {day}
    {separator}
    {month}
    {separator}
    {year}
)
"""

uk_pattern = re.compile(uk, re.X | re.I)

us = rf"""
(
    {month}
    {separator}
    {day}
    {separator}
    {year}
)
"""

us_pattern = re.compile(us, re.X | re.I)

docket_date_regex = rf"""
    (?P<docket_date>
        {us}|{uk}
    )
"""
