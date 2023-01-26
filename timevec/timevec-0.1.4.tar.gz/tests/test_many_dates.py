import timevec.numpy as tvn
import timevec.numpy_datetime64 as tv64
import timevec.builtin_math as tv
import numpy as np
import datetime

import pytest


def test_many_dates() -> None:
    # start 1-01-01
    dt = datetime.datetime(1, 1, 1, 0, 0, 0)

    # try all the functions does not raise an exception
    for i in range(50000):
        dt += datetime.timedelta(days=17, hours=13, minutes=11, seconds=7)
        yv = tv.year_vec(dt)
        tv.month_vec(dt)
        tv.week_vec(dt)
        dv = tv.day_vec(dt)
        assert pytest.approx(dt) == tv.datetime_from_vec(dt.year, yv, dv)

        yvn = tvn.year_vec(dt)
        tvn.month_vec(dt)
        tvn.week_vec(dt)
        dvn = tvn.day_vec(dt)
        assert pytest.approx(dt) == tvn.datetime_from_vec(dt.year, yvn, dvn)

        yv64 = tv64.year_vec(np.datetime64(dt))
        tv64.month_vec(np.datetime64(dt))
        tv64.week_vec(np.datetime64(dt))
        dv64 = tv64.day_vec(np.datetime64(dt))
        assert pytest.approx(np.datetime64(dt)) == tv64.datetime64_from_vec(dt.year, yv64, dv64)

    # tested up to 2100-01-01
    assert dt >= datetime.datetime(2400, 1, 1, 0, 0, 0)
