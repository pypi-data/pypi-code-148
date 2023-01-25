import os
import time


def set_timezone_to_norwegian_time():
    """sets python session timezone to norwegian time, linux only"""
    os.environ["TZ"] = "Europe/Oslo"
    time.tzset()  # pylint: disable=no-member
