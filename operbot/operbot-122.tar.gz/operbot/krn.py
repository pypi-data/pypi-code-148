# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0622


"kernel"


from opr.runtime import Cfg
from opr.objects import edit, fmt, keys, last, write


def krn(event):
    last(Cfg)
    if not Cfg.prs.txt:
        event.reply("config is empty")
        return
    if not event.sets:
        event.reply(fmt(
                        Cfg,
                        keys(Cfg),
                        skip="name,password,prs",
                       )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.done()
