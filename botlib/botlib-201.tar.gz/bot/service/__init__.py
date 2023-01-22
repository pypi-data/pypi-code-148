# This file is placed in the Public Domain.
# pylint: disable=E0401,W0406


"services"


from . import irc, rss, udp


def __dir__():
    return (
            "irc",
            "rss",
            "udp"
           )
 