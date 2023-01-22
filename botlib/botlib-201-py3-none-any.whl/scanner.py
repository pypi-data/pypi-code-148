# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402,W0613


"scanner"


import inspect
import os
import sys


from .handler import Command
from .objects import Class, Object
from .utility import spl


def __dir__():
    return (
            "scan",
            "scancls",
            "scancmd",
            "scanner",
            "scanpkg",
            "scandir"
           )


def include(name, namelist):
    for nme in namelist:
        if nme in name:
            return True
    return False


def initer(mname, path=None):
    mod = sys.modules.get(mname, None)
    if mod:
        mod.init()


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


def scanner(mname, path=None):
    mod = sys.modules.get(mname, None)
    if mod:
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


def scandir(path, func=scanner, pname=None, mods=None):
    res = []
    if pname is None:
        pname = path.split(os.sep)[-1]
    for modname in listmod(path):
        if not modname:
            continue
        if mods and not include(modname, spl(mods)):
            continue
        mname = "%s.%s" % (pname, modname)
        ppath = os.path.join(path, "%s.py" % modname)
        mod = func(mname, ppath)
        if mod:
            res.append(mod)
    return res


def scanpkg(pkg, func=scanner, mods=None):
    path = pkg.__path__[0]
    name = pkg.__name__
    return scandir(path, func, name, mods)
