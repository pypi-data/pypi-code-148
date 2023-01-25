from datetime import timedelta


def timedelta_to_hh_mm(delta: timedelta) -> str:
    '''
    Format a timedelta object to the following format:
    - Under 1 hour: 34m
    - Over 1 hour:  56h34m
    '''

    s = delta.total_seconds()
    h = int(s // 3600)
    m = int(s % 3600 // 60)
    if h > 0:
        return '{}h{:02}m'.format(h, m)
    else:
        return '{}m'.format(m)