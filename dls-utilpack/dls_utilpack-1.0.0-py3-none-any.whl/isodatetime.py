from datetime import datetime


def isodatetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def isodatetime_filename():
    return datetime.now().strftime("%Y-%m-%d.%H%M%S.%f")
