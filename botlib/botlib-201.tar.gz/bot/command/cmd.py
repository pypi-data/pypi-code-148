# This file is placed in the Public Domain.
# pylint: disable=C0116,E0402


"commands"


from ..handler import Command


def __dir__():
    return (
            'cmd',
           )


def cmd(event):
    event.reply(",".join(sorted(Command.cmd)))
