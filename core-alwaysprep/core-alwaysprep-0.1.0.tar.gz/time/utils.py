from datetime import datetime


def get_curent_time():
    return datetime.now().strftime("%H:%M:%S")
