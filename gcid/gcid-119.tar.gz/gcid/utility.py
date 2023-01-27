# This file is placed in the Public Domain.


"utility"


import getpass
import os
import pwd
import time
import types


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.4f}s"
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt.strip()
    if hours:
        txt += "%sh" % hours
    if minutes:
        txt += "%sm" % minutes
    if sec:
        txt += "%ss" % sec
    else:
        txt += "0s"
    txt = txt.strip()
    return txt


def name(obj):
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    return None


def privileges(username):
    if os.getuid() != 0:
        return
    try:
        pwnam = pwd.getpwnam(username)
    except KeyError:
        username = getpass.getuser()
        pwnam = pwd.getpwnam(username)
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def spl(txt):
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def wait(func=None):
    while 1:
        time.sleep(1.0)
        if func:
            func()
