# Test if the function implemented with numpy and the function implemented with builtin math return the same result.
from __future__ import annotations

import datetime

from typing import Callable, Tuple, List
import random
import timevec.builtin_math
import timevec.numpy
import numpy as np
import pytest


def assert_same(
    dt: datetime.datetime,
    func1: Callable[[datetime.datetime], Tuple[float, float]],
    func2: Callable[[datetime.datetime], np.ndarray],
    *,
    rel_tol: float = 1e-9,
    abs_tol: float = 0.0,
) -> None:
    dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    result1 = func1(dt)
    result2 = func2(dt)
    assert pytest.approx(result1[0], rel=rel_tol, abs=abs_tol) == result2[0]
    assert pytest.approx(result1[1], rel=rel_tol, abs=abs_tol) == result2[1]


def random_date() -> datetime.datetime:
    year = random.randint(1990, 2030)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.datetime(year, month, day, hour, minute, second)


def random_dates(size: int = 1000) -> List[datetime.datetime]:
    dates = []
    for _ in range(size):
        dates.append(random_date())
    return dates


def test_year_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, timevec.builtin_math.year_vec, timevec.numpy.year_vec)


def test_month_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, timevec.builtin_math.month_vec, timevec.numpy.month_vec)

    
def test_week_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, timevec.builtin_math.week_vec, timevec.numpy.week_vec)


def test_day_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, timevec.builtin_math.day_vec, timevec.numpy.day_vec)
