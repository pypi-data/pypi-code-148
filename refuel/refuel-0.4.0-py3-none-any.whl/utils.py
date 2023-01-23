from datetime import datetime, timedelta, timezone

REFUEL_DATE_FORMAT = "%Y-%m-%d"


def to_date_string(date_obj, fmt=REFUEL_DATE_FORMAT):
    return datetime.strftime(date_obj, fmt)


def get_datetime_offset(datetime_obj: datetime, delta: timedelta):
    return datetime_obj + delta


def current_utc_time():
    return datetime.now(timezone.utc)


DATE_FOURTEEN_DAYS_AGO = to_date_string(
    get_datetime_offset(current_utc_time(), -timedelta(days=14))
)
DATE_TOMORROW = to_date_string(
    get_datetime_offset(current_utc_time(), timedelta(days=1))
)
