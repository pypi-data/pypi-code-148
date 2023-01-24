from datetime import datetime
from pytz import timezone


def Get_Current_Date_Based_On_TimeZone(TimeZone, Format):
    """
                helper function to get the Current Date TimeZone
    """
    Current_Date = datetime.now(timezone(TimeZone)).strftime(Format)
    return Current_Date


def Get_Current_Time_Based_On_TimeZone(Tz):
    """
                helper function to get the Current Time ex: 'America/Chicago'
    """
    Current_Time = datetime.now(timezone(Tz)).strftime("%m/%d/%y %H:%M")
    return Current_Time
