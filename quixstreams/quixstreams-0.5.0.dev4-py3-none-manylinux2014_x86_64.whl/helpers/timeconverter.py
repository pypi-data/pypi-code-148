import sys
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
import logging


class TimeConverter:
    __epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    __epochNaive = datetime(1970, 1, 1)
    __epochTzInfo = __epoch.tzinfo
    __microsecond = timedelta(microseconds=1)

    __localTZInfo = None
    try:
        __localTZInfo = datetime.now().astimezone().tzinfo
    except:
        logging.warning("Timezone can't be determined, treating as UTC", exc_info=sys.exc_info())

    @staticmethod
    def to_unix_nanoseconds(value: datetime) -> int:
        if value.tzinfo is None:
            if TimeConverter.__localTZInfo is None:
                # the local time zone is something that is not supported, in this case there isn't much we can do
                # and treat is as naive datetime. Warning was logged by now
                return TimeConverter.to_nanoseconds(value - TimeConverter.__epochNaive)

            value = value.replace(tzinfo=TimeConverter.__localTZInfo)
        return TimeConverter.to_nanoseconds(value - TimeConverter.__epoch)

    @staticmethod
    def to_nanoseconds(value: timedelta) -> int:
        time = value / TimeConverter.__microsecond
        return int(time * 1000)

    @staticmethod
    def from_nanoseconds(value: int) -> timedelta:
        time = value / 1000
        return timedelta(microseconds=time)

    @staticmethod
    def from_unix_nanoseconds(value: int) -> datetime:
        return TimeConverter.__epoch + TimeConverter.from_nanoseconds(value)

    @staticmethod
    def from_string(value: str) -> int:
        if value is None:
            return 0
        if value.isnumeric():
            return int(value)

        dt = parse(value)
        return TimeConverter.to_unix_nanoseconds(dt)
