import datetime

import pytest

from timevec.builtin_math import day_vec, month_vec, week_vec, year_vec


def test_year_vec() -> None:
    # 0 degrees at the beginning of the year
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # 180 degrees at the middle of the year
    dt = datetime.datetime(2023, 7, 2, 12, 0, 0)
    x, y = year_vec(dt)
    assert (x, y) == pytest.approx((-1.0, 0.0), abs=1e-6)

    # 360 degrees at the end of the year
    dt = datetime.datetime(2023, 12, 31, 23, 59, 59)
    x, y = year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_month_vec() -> None:
    # 0 degrees at the beginning of the month
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = month_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # 180 degrees at the middle of the month
    dt = datetime.datetime(2023, 1, 16, 12, 0, 0)
    x, y = month_vec(dt)
    assert (x, y) == pytest.approx((-1.0, 0.0), abs=1e-6)

    # 360 degrees at the end of the month
    dt = datetime.datetime(2023, 1, 31, 23, 59, 59)
    x, y = month_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-5)


def test_week_vec() -> None:
    # 0 degrees at the beginning of the week
    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)  # Monday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 3, 0, 0, 0)  # Tuesday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((0.623489, 0.781831), abs=1e-6)

    dt = datetime.datetime(2023, 1, 4, 0, 0, 0)  # Wednesday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((-0.222521, 0.974928), abs=1e-6)

    dt = datetime.datetime(2023, 1, 5, 0, 0, 0)  # Thursday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((-0.900969, 0.433884), abs=1e-6)

    dt = datetime.datetime(2023, 1, 6, 0, 0, 0)  # Friday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((-0.900969, -0.433884), abs=1e-6)

    dt = datetime.datetime(2023, 1, 7, 0, 0, 0)  # Saturday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((-0.222521, -0.974928), abs=1e-6)

    dt = datetime.datetime(2023, 1, 8, 0, 0, 0)  # Sunday
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((0.623489, -0.781831), abs=1e-6)

    # next monday
    dt = datetime.datetime(2023, 1, 9, 0, 0, 0)
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_day_vec() -> None:
    # 0 degrees at the beginning of the day
    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)
    x, y = day_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # 180 degrees at the middle of the day
    dt = datetime.datetime(2023, 1, 2, 12, 0, 0)
    x, y = day_vec(dt)
    assert (x, y) == pytest.approx((-1.0, 0.0), abs=1e-6)

    # 360 degrees at the almost end of the day
    dt = datetime.datetime(2023, 1, 2, 23, 59, 59, 999999)
    x, y = day_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)


def test_edge_cases() -> None:
    # beginning of year
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    x, y = month_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)
    x, y = week_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)
    x, y = day_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)

    # end of year
    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    x, y = year_vec(dt)
    assert (x, y) == pytest.approx((1.0, 0.0), abs=1e-6)
