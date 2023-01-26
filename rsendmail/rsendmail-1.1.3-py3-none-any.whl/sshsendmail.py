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
import copy
import logging
import logging.handlers
import os
import subprocess
import sys

__description__ = """nullmailer-rsendmail compatibility shim."""


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, epilog=__description__)
    parser.add_argument(
        "--loglevel",
        dest="loglevel",
        default="WARNING",
        help="level should be sent to syslog (default: %(default)s)",
    )
    default_mta = "postfix"
    if "nullmailer" in os.path.realpath(sys.argv[0]):
        default_mta = "nullmailer"
    parser.add_argument(
        "--mta",
        choices=["postfix", "nullmailer"],
        default=default_mta,
        help="communication interface with parent MTA (default: %(default)s)",
    )
    parser.add_argument("--identity", help="path to SSH private key")
    parser.add_argument("--user", help="username for the SSH host")
    parser.add_argument("--host", help="remote email gateway running rsendmail")
    parser.add_argument("-f", dest="sender", help="enveloper sender")
    parser.add_argument(
        "-d",
        "-s",
        dest="nullmailer1",
        action="store_true",
        help="arguments passed by nullmailer1, triggers an exception",
    )
    parser.add_argument(
        "recipients",
        nargs="*",
        help="who to send the email to, may be parsed from MTA-specific headers instead",
    )
    args = parser.parse_args()
    if args.mta != "nullmailer" and not args.host:
        parser.error("a remote host should be provided as --host")
    if args.nullmailer1:
        parser.error("nullmailer 1 flags detected, aborting")
    return args


def setupLogging(syslog):
    logger = logging.getLogger("")
    # disable the base filter, each stream has its own filter
    logger.setLevel("DEBUG")
    sl = logging.handlers.SysLogHandler(address="/dev/log", facility="mail")
    sl.setFormatter(
        logging.Formatter(sys.argv[0] + "[%(process)d]: %(levelname)s: %(message)s")
    )
    # convert syslog argument to a numeric value
    sl.setLevel(syslog.upper())
    logger.addHandler(sl)


def readNullMailer2Options(args, stream):
    """read nullmailer configuration

    nullmailer sends its configuration on stdin with one option per
    line, in key=value pairs separated by equal signs. we parse from
    the ``stream`` argument to facilitate tests.

    store the resulting config in the ``args`` namespace.
    """
    for line in stream:
        # this block ends on an empty line
        line = line.strip()
        logging.debug("got config from nullmailer: %s", line)
        if line == "":
            break
        if "=" in line:
            name, val = line.split("=", 1)
            setattr(args, name, val)
        else:
            logging.warning("unexpected config syntax from nullmailer: %s", line)


def readNullMailer2Envelope(stream):
    """read envelope information from nullmailer

    nullmailer sends addresses one per line. the first address is the
    "envelope sender address", who to send errors to and equivalent to
    the `-f` sendmail flag. then the remaining lines are recipients.

    extract the sender and recipients, which are return as a tuple.
    """
    sender = None
    recipients = []
    try:
        for line in stream:
            line = line.strip()
            logging.debug("got envelope from nullmailer: %s", line)
            # the envelope block ends on an empty line
            if line == b"":
                break
            assert (
                len(line) > 3
            ), "sanity check: emails are generally longer than three characters"

            if not sender:
                # first the sender...
                sender = line.decode(errors="backslashreplace")
            else:
                # ... then the recipients
                recipients.append(line.decode(errors="backslashreplace"))
    except OSError as e:
        # this error was triggered when called with nullmailer 1.
        # this should not happen anymore as nullmailer 1 passes the -d
        # or -s flags which we abort on since 743e584 but checking
        # anyways shouldn't hurt
        if "read() should have returned a bytes object, not 'NoneType'" in str(e):
            logging.error(
                "cannot open file descriptor 3, are you running nullmailer 2.x?"
            )
    return sender, recipients


# map error codes from sendmail to nullmailer
nullmailer_sysexits_map = {
    os.EX_OK: "EX_OK",  # Successful completion on all addresses.
    # ssh returns the remote command status code, unless the command
    # cannot be ran, in which case it returns this:
    255: "ERR_CONN_FAILED",
    # those are defined in sendmail(8) manpage (v8.15.2)
    os.EX_NOUSER: "ERR_MSG_REFUSED",  # User name not recognized.
    os.EX_UNAVAILABLE: "ERR_EXEC_FAILED",  # Catchall meaning necessary resources were not available.
    # not in Python or Debian
    # os.EX_SYNTAX: 'ERR_MSG_REFUSED',     # Syntax error in address.
    os.EX_SOFTWARE: "ERR_USAGE",  # Internal software error, including bad arguments.
    os.EX_OSERR: "ERR_EXEC_FAILED",  # Temporary operating system error, such as ``cannot fork''.
    os.EX_NOHOST: "ERR_NO_ADDRESS",  # Host name not recognized.
    # os.EX_TEMPFAIL is ignored for sendmail, because it is "Message
    # could not be sent immediately, but was queued." That is nuts:
    # this is not an error, it is what mail servers do. They queue up
    # mail. Leave room for reasonable mail server errors and ignore
    # old sendmail here.
    #
    # postfix exit codes, as read in the sendmail.c source code in
    # Postfix 3.3.0
    1: "ERR_USAGE",  # 1: if daemon mode fails
    os.EX_TEMPFAIL: "ERR_MSG_TEMPFAIL",  # failed to write queue file, etc
    os.EX_NOPERM: "ERR_MSG_REFUSED",  # User %s(%ld) is not allowed to submit mail
    os.EX_USAGE: "ERR_USAGE",  # problem with the arguments passed to Postfix
    os.EX_DATAERR: "ERR_USAGE",  # unable to extract recipients, error reading input
    # already covered above:
    # EX_OSERR: no login name found for user ID, fail to open /dev/null
    # EX_UNAVAILABLE: can't exec postdrop, can't fork, can't chdir, etc
    # EX_SOFTWARE
    #
    # Exim returns 0 or 1 (so always temporary), covered above.
    #
    # opensmtpd also uses EX_* macros, all covered above
    #
    # qmail
    100: "ERR_USAGE",  # newaliases, usage
    111: "ERR_EXEC_FAILED",  # can't run some part of qmail
}

# python version of `lib/errcodes.h` from nullmailer 2.1
nullmailer_error_table = {
    # not part of nullmailer, but should be.
    "EX_OK": os.EX_OK,
    # temporary errors are < 32
    "ERR_USAGE": 1,  # Invalid command-line arguments
    "ERR_HOST_NOT_FOUND": 2,  # gethostbyname failed with HOST_NOT_FOUND
    "ERR_NO_ADDRESS": 3,  # gethostbyname failed with NO_ADDRESS
    "ERR_GHBN_TEMP": 5,  # gethostbyname failed with TRY_AGAIN
    "ERR_SOCKET": 6,  # socket failed
    "ERR_CONN_REFUSED": 7,  # connect failed with ECONNREFUSED
    "ERR_CONN_TIMEDOUT": 8,  # connect failed with ETIMEDOUT
    "ERR_CONN_UNREACHABLE": 9,  # connect failed with ENETUNREACH
    "ERR_CONN_FAILED": 10,  # connect failed
    "ERR_PROTO": 11,  # unexpected result from server
    "ERR_MSG_OPEN": 12,  # could not open the message
    "ERR_MSG_READ": 13,  # reading the message failed
    "ERR_MSG_WRITE": 14,  # writing the message failed
    "ERR_EXEC_FAILED": 15,  # executing a program failed
    "ERR_MSG_TEMPFAIL": 16,  # server temporarily failed to receive
    "ERR_UNKNOWN": 17,  # Arbitrary error code
    "ERR_CONFIG": 18,  # Error reading a config file
    "ERR_BIND_FAILED": 19,  # Failed to bind source address
    # Permanent errors are >= 32
    "ERR_PERMANENT_FLAG": 32,
    "ERR_GHBN_FATAL": 33,  # gethostbyname failed with NO_RECOVERY
    "ERR_MSG_REFUSED": 34,  # server refused the message
    "ERR_MSG_PERMFAIL": 35,  # server permanently failed to receive
}


def main():
    argv = copy.copy(sys.argv)
    args = parse_args()
    setupLogging(args.loglevel)

    logging.debug("config: %s", args)
    if args.mta == "nullmailer":
        logging.debug("argv: %s", argv)
        readNullMailer2Options(args, sys.stdin)
        logging.debug("modified config: %s", args)

        # need unbuffered I/O otherwise parts of the message will be
        # swallowed before being passed to the subprocess
        message = open(3, mode="rb", buffering=0)
        args.sender, args.recipients = readNullMailer2Envelope(message)
    elif args.mta == "postfix":
        message = sys.stdin
    else:
        # should not happen
        logging.error("unsupported MTA: %s", args.mta)
        return 1

    # compose base command
    command = ["ssh", args.host]
    if args.identity:
        command += ["-i", args.identity]
    if args.user:
        command += ["-l", args.user]

    # remote command
    remote_command = ["rsendmail"]
    if args.sender:
        remote_command += ["-f", args.sender]
    if args.recipients:
        remote_command += args.recipients
    command.append(" ".join(remote_command))

    logging.info("sending email through %s", command)
    process = subprocess.Popen(command, shell=False, close_fds=False, stdin=message)
    status = process.wait()
    if status != 0:
        logging.error("command failed with exit status %d: %s", status, command)

    if args.mta == "nullmailer":
        # map rsendmail error codes to nullmailer. default to temporary.
        return nullmailer_error_table[
            nullmailer_sysexits_map.get(status, "ERR_UNKNOWN")
        ]
    elif args.mta == "postfix":
        # SSH will return code 255 on *any* failure, treat those as temporary
        if status == 255:
            return os.EX_TEMPFAIL
        # otherwise error codes are from rsendmail, which passes them
        # from sendmail, so this should be in sysexits.h and processed
        # properly by Postfix, as per
        # postfix-3.3.0/src/global/pipe_command.c
        else:
            return status
    else:
        # NOTREACHED
        return os.EX_SOFTWARE


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logging.exception("got exception %s", e)
        sys.exit(1)
