import datetime

import numpy as np
import numpy.typing as npt

from timevec.numpy import datetime_from_vec, ratio_to_vec
from timevec.util import (
    day_range,
    month_range,
    time_elapsed_ratio,
    week_range,
    year_range,
)


def year_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    dt2 = datetime64_to_datetime(dt)
    begin_of_year, end_of_year = year_range(dt2)
    rate = time_elapsed_ratio(
        begin=begin_of_year,
        end=end_of_year,
        current=dt2,
    )
    return ratio_to_vec(rate, dtype=dtype)


def month_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the month as a vector"""
    dt2 = datetime64_to_datetime(dt)
    begin_of_month, end_of_month = month_range(dt2)
    rate = time_elapsed_ratio(
        begin=begin_of_month,
        end=end_of_month,
        current=dt2,
    )
    return ratio_to_vec(rate, dtype=dtype)


def week_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the week as a vector"""
    dt2 = datetime64_to_datetime(dt)
    begin_of_week, end_of_week = week_range(dt2)
    rate = time_elapsed_ratio(
        begin=begin_of_week,
        end=end_of_week,
        current=dt2,
    )
    return ratio_to_vec(rate, dtype=dtype)


def day_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the day as a vector"""
    dt2 = datetime64_to_datetime(dt)
    begin_of_day, end_of_day = day_range(dt2)
    rate = time_elapsed_ratio(
        begin=begin_of_day,
        end=end_of_day,
        current=dt2,
    )
    return ratio_to_vec(rate, dtype=dtype)


def datetime64_to_datetime(dt: np.datetime64) -> datetime.datetime:
    """Convert a numpy.datetime64 to a datetime.datetime"""
    dt64 = np.datetime64(dt)
    ts = float(
        (dt64 - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
    )
    return datetime.datetime.utcfromtimestamp(ts)


def datetime64_from_vec(
    year: int,
    yv: npt.NDArray,
    dv: npt.NDArray,
) -> np.datetime64:
    """Convert a vector representation of a datetime to a numpy.datetime64"""
    dt = datetime_from_vec(year, yv, dv)
    return np.datetime64(dt)
