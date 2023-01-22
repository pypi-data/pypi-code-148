# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402


"list bots"


from ..handler import Bus
from ..threads import name


def __dir__():
    return (
            'flt',
           )


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([name(o) for o in Bus.objs]))
