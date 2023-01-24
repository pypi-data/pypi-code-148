import datetime
import math
from typing import Tuple

from timevec.util import (
    day_range,
    month_range,
    time_elapsed_ratio,
    week_range,
    year_range,
)


def year_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the year as a vector"""
    begin_of_year, end_of_year = year_range(dt)
    rate = time_elapsed_ratio(begin=begin_of_year, end=end_of_year, current=dt)
    return ratio_to_vec(rate)


def month_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the month as a vector"""
    begin_of_month, end_of_month = month_range(dt)
    rate = time_elapsed_ratio(
        begin=begin_of_month, end=end_of_month, current=dt
    )
    return ratio_to_vec(rate)


def week_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the week as a vector"""
    # weekday is 0 for Monday and 6 for Sunday
    begin_of_week, end_of_week = week_range(dt)
    rate = time_elapsed_ratio(begin=begin_of_week, end=end_of_week, current=dt)
    return ratio_to_vec(rate)


def day_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the day as a vector"""
    begin_of_day, end_of_day = day_range(dt)
    rate = time_elapsed_ratio(begin=begin_of_day, end=end_of_day, current=dt)
    return ratio_to_vec(rate)


def ratio_to_vec(rate: float) -> Tuple[float, float]:
    s = 2 * math.pi * rate
    x = math.cos(s)
    y = math.sin(s)
    return x, y
