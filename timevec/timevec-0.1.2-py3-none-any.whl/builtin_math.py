import calendar
import datetime
import math
from typing import Tuple


def year_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the year as a vector"""
    begin_of_year = datetime.datetime.min.replace(
        year=dt.year, month=1, day=1, hour=0, minute=0, second=0
    )
    end_of_year = datetime.datetime.min.replace(
        year=dt.year + 1, month=1, day=1, hour=0, minute=0, second=0
    )
    rate = time_elapsed_ratio(begin=begin_of_year, end=end_of_year, current=dt)
    return ratio_to_vec(rate)


def month_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the month as a vector"""
    begin_of_month = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=1, hour=0, minute=0, second=0
    )
    _, last_day = calendar.monthrange(dt.year, dt.month)
    end_of_month = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=last_day, hour=0, minute=0, second=0
    ) + datetime.timedelta(days=1)
    rate = time_elapsed_ratio(
        begin=begin_of_month, end=end_of_month, current=dt
    )
    return ratio_to_vec(rate)


def week_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the week as a vector"""
    # weekday is 0 for Monday and 6 for Sunday
    begin_of_week = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0
    ) - datetime.timedelta(days=dt.weekday())
    end_of_week = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0
    ) + datetime.timedelta(days=7 - dt.weekday())
    rate = time_elapsed_ratio(begin=begin_of_week, end=end_of_week, current=dt)
    return ratio_to_vec(rate)


def day_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the day as a vector"""
    begin_of_day = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0
    )
    end_of_day = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0
    ) + datetime.timedelta(days=1)
    rate = time_elapsed_ratio(begin=begin_of_day, end=end_of_day, current=dt)
    return ratio_to_vec(rate)


def time_elapsed_ratio(
    *,
    begin: datetime.datetime,
    end: datetime.datetime,
    current: datetime.datetime,
) -> float:
    total_seconds = (end - begin).total_seconds()
    elapsed_time = (current - begin).total_seconds()
    return elapsed_time / total_seconds


def ratio_to_vec(rate: float) -> Tuple[float, float]:
    s = 2 * math.pi * rate
    x = math.cos(s)
    y = math.sin(s)
    return x, y
