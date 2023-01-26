import calendar
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


def vec_to_ratio(x: float, y: float) -> float:
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    angle = math.atan2(y, x) / (2.0 * math.pi)
    return angle if angle >= 0 else angle + 1.0


def datetime_from_vec(
    year: int,
    yv: Tuple[float, float],
    dv: Tuple[float, float],
) -> datetime.datetime:
    position_in_year = vec_to_ratio(*yv)
    position_in_day = vec_to_ratio(*dv)
    d = int(position_in_year * (366.0 if calendar.isleap(year) else 365.0))
    s = position_in_day * 86400.0
    return datetime.datetime(year, 1, 1, 0, 0, 0, 0) + datetime.timedelta(
        days=int(d), seconds=s
    )
