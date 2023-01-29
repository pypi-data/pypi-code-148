from .utils import get_default_year


def is_valid_year(year: str):
    try:
        year = int(year)
        return year >= 2015 and year <= get_default_year()
    except ValueError:
        return False

def is_valid_day(day: str):
    try:
        day = int(day)
        return day in range(1, 26)
    except ValueError:
        return False

