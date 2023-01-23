from datetime import datetime


class AppleDateTime(object):
    @staticmethod
    def datetime(time_string: str) -> datetime:
        timestamp_without_timezone = time_string.split(' +')[0]
        return datetime.strptime(timestamp_without_timezone, '%Y-%m-%d %H:%M:%S.%f')
