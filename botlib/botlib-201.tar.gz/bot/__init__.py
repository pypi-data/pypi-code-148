# This file is placed in the Public Domain.
# pylint: disable=W0622,W0406,E0401


"The Python3 bot Namespace"


from . import command, handler, modules, objects, runtime, scanner, service
from . import threads


from .objects import *


def __dir__():
    return (
            "command",
            "handler",
            "message",
            "modules",
            "objects",
            "runtime",
            "scanner",
            'service',
            "threads"
           )
