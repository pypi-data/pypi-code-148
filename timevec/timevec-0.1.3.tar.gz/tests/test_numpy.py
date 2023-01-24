import datetime

import numpy as np
import pytest

from timevec.numpy import day_vec, month_vec, week_vec, year_vec


def test_year_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 7, 2, 12, 0, 0)
    vec = year_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 12, 31, 23, 59, 59)
    vec = year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)


def test_month_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 16, 12, 0, 0)
    vec = month_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 31, 23, 59, 59)
    vec = month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-5)


def test_week_vec() -> None:
    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)  # Monday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 3, 0, 0, 0)  # Tuesday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([0.623489, 0.781831]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 4, 0, 0, 0)  # Wednesday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([-0.222521, 0.974928]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 5, 0, 0, 0)  # Thursday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([-0.900969, 0.433884]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 6, 0, 0, 0)  # Friday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([-0.900969, -0.433884]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 7, 0, 0, 0)  # Saturday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([-0.222521, -0.974928]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 8, 0, 0, 0)  # Sunday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([0.623489, -0.781831]), abs=1e-6)


def test_day_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = day_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
    vec = day_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)


def test_edge_cases() -> None:
    # beginning of year
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)  # Monday
    vec = week_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = day_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    # end of year
    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    vec = year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    vec = month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-5)

    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    vec = day_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-4)

    # end of month
    dt = datetime.datetime(2023, 1, 31, 23, 59, 59, 999999)
    vec = month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-5)
