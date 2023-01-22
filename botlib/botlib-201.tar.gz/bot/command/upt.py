# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402


"uptime"


import time


from ..utility import elapsed


def __dir__():
    return (
            'upt'
           )


starttime = time.time()


def upt(event):
    event.reply(elapsed(time.time()-starttime))
