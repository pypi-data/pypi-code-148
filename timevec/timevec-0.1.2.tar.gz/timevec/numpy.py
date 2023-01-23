import calendar
import datetime

import numpy as np
import numpy.typing as npt

from timevec.builtin_math import time_elapsed_ratio


def year_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    begin_of_year = datetime.datetime(
        dt.year, month=1, day=1, hour=0, minute=0, second=0
    )
    end_of_year = datetime.datetime(
        dt.year + 1, month=1, day=1, hour=0, minute=0, second=0
    )
    rate = time_elapsed_ratio(
        begin=begin_of_year,
        end=end_of_year,
        current=dt,
    )
    return ratio_to_vec(rate, dtype=dtype)


def month_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the month as a vector"""
    begin_of_month = datetime.datetime(
        year=dt.year, month=dt.month, day=1, hour=0, minute=0, second=0
    )
    _, last_day = calendar.monthrange(dt.year, dt.month)
    end_of_month = datetime.datetime(
        year=dt.year, month=dt.month, day=last_day, hour=0, minute=0, second=0
    ) + datetime.timedelta(days=1)
    rate = time_elapsed_ratio(
        begin=begin_of_month,
        end=end_of_month,
        current=dt,
    )
    return ratio_to_vec(rate, dtype=dtype)


def week_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the week as a vector"""
    begin_of_week = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) - datetime.timedelta(days=dt.weekday())
    end_of_week = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=7 - dt.weekday())
    rate = time_elapsed_ratio(
        begin=begin_of_week,
        end=end_of_week,
        current=dt,
    )
    return ratio_to_vec(rate, dtype=dtype)


def day_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the day as a vector"""
    begin_of_day = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_day = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=1)
    rate = time_elapsed_ratio(
        begin=begin_of_day,
        end=end_of_day,
        current=dt,
    )
    return ratio_to_vec(rate, dtype=dtype)


def ratio_to_vec(
    ratio: float, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the ratio as a vector"""
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2.0 * np.pi * ratio)
    vec[1] = np.sin(2.0 * np.pi * ratio)
    return vec
