import calendar
import datetime

import numpy as np
import numpy.typing as npt

from timevec.util import (
    day_range,
    month_range,
    time_elapsed_ratio,
    week_range,
    year_range,
)


def year_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    begin_of_year, end_of_year = year_range(dt)
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
    begin_of_month, end_of_month = month_range(dt)
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
    begin_of_week, end_of_week = week_range(dt)
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
    begin_of_day, end_of_day = day_range(dt)
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


def vec_to_ratio(arr: npt.NDArray) -> float:
    """Convert a vector to a ratio"""
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    base = np.arctan2(arr[1], arr[0]) / (2.0 * np.pi)
    return float(base if base >= 0.0 else base + 1.0)


def datetime_from_vec(
    year: int,
    yv: npt.NDArray,
    dv: npt.NDArray,
) -> datetime.datetime:
    position_in_year = vec_to_ratio(yv)
    position_in_day = vec_to_ratio(dv)
    d = int(position_in_year * (366.0 if calendar.isleap(year) else 365.0))
    s = position_in_day * 86400.0
    delta = datetime.timedelta(days=d, seconds=s)
    return datetime.datetime(year, 1, 1, 0, 0, 0, 0) + delta
