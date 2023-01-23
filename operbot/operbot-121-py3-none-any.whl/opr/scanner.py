# This file is placed in the Public Domain.


"scanner"


import inspect
import os
import sys


from .handler import Command
from .objects import Class, Object
from .threads import launch
from .utility import spl


def __dir__():
    return (
            "scan",
            "scancls",
            "scancmd",
            "scanpkg",
            "scandir"
           )


def include(name, namelist):
    for nme in namelist:
        if nme in name:
            return True
    return False


def listmod(path):
    res = []
    if not os.path.exists(path):
        return res
    for fnm in os.listdir(path):
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        res.append(fnm.split(os.sep)[-1][:-3])
    return res


def scan(mod):
    scancls(mod)
    scancmd(mod)


def scancls(mod):
    for key, obj in inspect.getmembers(mod, inspect.isclass):
        if key.startswith("cb"):
            continue
        if issubclass(obj, Object):
            Class.add(obj)


def scancmd(mod):
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)


def scandir(path, pname=None, mods=None, init=False):
    res = []
    thrs = []
    if pname is None:
        pname = path.split(os.sep)[-1]
    for modname in listmod(path):
        if not modname:
            continue
        if mods and not include(modname, spl(mods)):
            continue
        mname = "%s.%s" % (pname, modname)
        mod = sys.modules.get(mname, None)
        if mod:
            scan(mod)
            res.append(mod)
            if init and "init" in dir(mod):
                thrs.append(launch(mod.init))
    for thr in thrs:
        thr.join()
    return res


def scanpkg(pkg, mods=None, init=True):
    path = pkg.__path__[0]
    name = pkg.__name__
    return scandir(path, name, mods, init)
