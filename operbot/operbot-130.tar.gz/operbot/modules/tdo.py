# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903


"todo"


import time


from ..objects import Class, Object, find, fntime, save, write
from ..utility import elapsed


def __dir__():
    return (
            'Todo',
            'dne',
            'tdo'
           )


class Todo(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ""


Class.add(Todo)


def dne(event):
    if not event.args:
        event.reply("dne txt==<string>")
        return
    selector = {"txt": event.args[0]}
    for obj in find("todo", selector):
        obj.__deleted__ = True
        write(obj)
        event.done()
        break

def tdo(event):
    if not event.rest:
        nmr = 0
        for obj in find("todo"):
            event.reply("%s %s %s" % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(obj.__fnm__))
                                     ))
            nmr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    save(obj)
    event.done()
