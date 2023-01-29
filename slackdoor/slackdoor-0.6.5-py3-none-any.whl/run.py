import argparse
import asyncio
import logging
import os
import sys

from typing import NoReturn

from door import core


def main() -> NoReturn:
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="include debug logging")
    ap.add_argument("-o", "--stdout", action="store_true", help="log to stdout (instead of just errors to stderr)")
    ap.add_argument("-w", "--warnings", action="store_true", help="log only warnings and above")
    args = ap.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    elif args.warnings:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO

    # When running as console entry point, current working dir is not in Python path, so add it
    sys.path.insert(0, os.getcwd())

    core.start(asyncio.new_event_loop(), log_level=log_level, stdout=args.stdout)

    sys.exit(0)
