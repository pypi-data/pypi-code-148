import calendar
import datetime
from typing import Tuple


def year_range(
    dt: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime]:
    begin_of_year = datetime.datetime.min.replace(
        year=dt.year,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_year = datetime.datetime.min.replace(
        year=dt.year + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return begin_of_year, end_of_year


def month_range(
    dt: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime]:
    begin_of_month = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    _, last_day = calendar.monthrange(dt.year, dt.month)
    end_of_month = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=last_day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=1)
    return begin_of_month, end_of_month


def week_range(
    dt: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime]:
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
    return begin_of_week, end_of_week


def day_range(
    dt: datetime.datetime,
) -> Tuple[datetime.datetime, datetime.datetime]:
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
    return begin_of_day, end_of_day


def time_elapsed_ratio(
    *,
    begin: datetime.datetime,
    end: datetime.datetime,
    current: datetime.datetime,
) -> float:
    total_seconds = (end - begin).total_seconds()
    elapsed_time = (current - begin).total_seconds()
    return elapsed_time / total_seconds
