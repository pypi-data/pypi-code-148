from datetime import datetime, date, time, timezone


class DateFunctions:
    @staticmethod
    def date_to_unix_millis(d: date):
        return datetime.combine(d, time()).astimezone(timezone.utc).timestamp() * 1000
