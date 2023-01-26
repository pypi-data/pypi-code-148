#!/usr/bin/python3
# coding: utf-8

"""A safer sendmail command"""

# Copyright (C) 2017 Antoine Beaupré <anarcat@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import argparse
import logging
import logging.handlers
import os
import shlex
import subprocess
import sys

__description__ = """A wrapper for the sendmail command which allows calling sendmail
without allowing side effects traditionnally allowed by sendmail
binaries (like flushing the queue or reloading the alias files). This
is designed to be ran from an SSH command and be safely assigned
as a authorized_keys `command=` parameter."""


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, epilog=__description__)
    parser.add_argument(
        "--loglevel",
        dest="loglevel",
        default="INFO",
        help="level should be sent to syslog (default: %(default)s)",
    )
    parser.add_argument(
        "-oi",
        dest="passthrough",
        action=StoreFlagAction,
        help="(Ignored) When reading a message from standard input, don´t treat a"
        "line with only a . character as the end of input.",
    )
    parser.add_argument(
        "-f",
        dest="passthrough",
        action=StoreFlagAction,
        nargs=1,
        help="Set the envelope sender address. This is the address where"
        "delivery problems are sent to. Passed to sendmail.",
    )
    # XXX: would be better to have a "passthru" action or something
    parser.add_argument(
        "-t",
        dest="passthrough",
        action=StoreFlagAction,
        help="Extract recipients from message headers. These are added to any"
        "recipients specified on the command line. Passed to sendmail, no"
        "processing is done by rsendmail.",
    )
    parser.add_argument("recipient", nargs="*", help="recipients of the message")
    argv = os.environ.get("SSH_ORIGINAL_COMMAND", None)
    if argv:
        argv = shlex.split(argv)[1:]
    return parser.parse_args(argv)


class StoreFlagAction(argparse.Action):
    """store the provided flag in the destination

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('-t', dest='p', action=StoreFlagAction) # doctest: +ELLIPSIS
    StoreFlagAction(...)
    >>> parser.add_argument('-f', dest='p', nargs=1, action=StoreFlagAction) # doctest: +ELLIPSIS
    StoreFlagAction(...)
    >>> parser.parse_args([])
    Namespace(p=[])
    >>> parser.parse_args(['-t'])
    Namespace(p=['-t'])
    >>> parser.parse_args(['-t', '-f', 'foo'])
    Namespace(p=['-t', '-f', 'foo'])
    """

    def __init__(self, *args, **kwargs):
        kwargs["nargs"] = kwargs.get("nargs", 0)
        super().__init__(*args, default=[], **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string:
            items = getattr(namespace, self.dest, [])
            if not items:
                items = []
            items.append(option_string)
            if values:
                items += values
            setattr(namespace, self.dest, items)


def filter_args(args):
    """find arguments in list that have possibly nasty side effects

    >>> list(filter_args(['-f', 'foo']))
    ['-f']
    """
    for arg in args:
        if arg.startswith("-") or " " in arg:
            yield arg


def setupLogging(loglevel):
    logger = logging.getLogger("")
    # disable the base filter, each stream has its own filter
    logger.setLevel(loglevel)
    sl = logging.handlers.SysLogHandler(address="/dev/log", facility="mail")
    sl.setFormatter(
        logging.Formatter(sys.argv[0] + "[%(process)d]: %(levelname)s: %(message)s")
    )
    logger.addHandler(sl)
    st = logging.StreamHandler()
    logger.addHandler(st)


def main():
    args = parse_args()
    setupLogging(args.loglevel)

    bad = list(filter_args(args.recipient))
    if bad:
        logging.error(
            'email addresses cannot start with a dash ("-") or contain spaces: %s', bad
        )
        return 1
    # make sure we also look in /usr/sbin as it is often where sendmail is located
    if "/usr/sbin" not in os.get_exec_path():
        os.environ["PATH"] += ":/usr/sbin"
    command = ["sendmail"] + args.passthrough + args.recipient
    logging.debug("sending message through command: %s", command)
    process = subprocess.Popen(command, shell=False, stdin=sys.stdin, close_fds=True)
    status = process.wait()
    # those statuses and come from the SMTP standard, RFC 3463. They
    # are used liberally here, as a fallback when the `sshsendmail`
    # command isn't used on the other end, in which case Postfix will
    # parse the first line of the output looking for such an "enhanced
    # status code". Those are also useful for debugging as they will
    # show up in mail logs.
    if status == 0:
        logging.info("2.0.0 message sent through command: %s", command)
    else:
        # 4 means temporary, 3.5 means "The system is not configured
        # in a manner that will permit it to accept this message." It
        # is a generic error that was picked because it is otherwise
        # not possible to determine the actual error from the sendmail
        # return codes, or, more exactly, we already do that level of
        # parsing in sshsendmail and do not want to duplicate that
        # here.
        logging.error(
            "4.3.5 failed to send message with status code %d through command: %s",
            status,
            command,
        )
    return status


if __name__ == "__main__":
    sys.exit(main())
