import datetime


def percent(nb):
    """Format the number sent into a % number."""
    the_number = round(100 * nb, 2)
    the_string = '{: >6.2f}%'.format(the_number)
    return the_string


def now():
    """Get current timestamp in seconds (number)."""
    return  int(datetime.datetime.now().timestamp())
