# This file is placed in the Public Domain.


"find"


import time


from gcid.objects import Wd, find, fmt, fntime, keys
from gcid.utility import elapsed


def __dir__():
    return (
            "fnd",
           )


def fnd(event):
    if not event.args:
        res = ",".join(sorted([x.split(".")[-1].lower() for x in Wd.types()]))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    otype = event.args[0]
    nmr = 0
    keyz = None
    if event.gets:
        keyz = ",".join(keys(event.gets))
    if len(event.args) > 1:
        keyz += "," + ",".join(event.args[1:])
    for obj in find(otype, event.gets):
        if not keyz:
            keyz = "," + ",".join(keys(obj))
        txt = "%s %s %s" % (
                            str(nmr),
                            fmt(obj, keyz, event.toskip),
                            elapsed(time.time()-fntime(obj.__fnm__))
                           )
        nmr += 1
        event.reply(txt)
    if not nmr:
        event.reply("no result (%s)" % event.txt)
