import argparse
import datetime
import json
import sys
import uuid
from base64 import b64encode
from io import BufferedReader, TextIOWrapper
from typing import Any, Callable, Iterable

import llsd


def format_binary(v: Any):
    """
    Format binary with no LLSD header.

    Workaround for inconsistent parse_* method behavior in llsd module.
    """
    return llsd.format_binary(v).lstrip(b'<?llsd/binary?>\n')


class JSONEncoder(json.JSONEncoder):
    """JSON encoder with support for reading LLSD-parsed types"""
    def default(self, v: Any):
        if isinstance(v, uuid.UUID):
            return str(v)
        elif isinstance(v, datetime.datetime):
            return v.isoformat()
        elif isinstance(v, bytes):
            return b64encode(v).decode("ascii")
        return super(JSONEncoder, self).default(v)


def llsd2json(argv: Iterable[str] = None):
    parser = argparse.ArgumentParser(description="Convert LLSD to JSON")
    parser.add_argument(
        "input",
        nargs="?",
        default=(None if sys.stdin.isatty() else sys.stdin.buffer),
        help="LLSD string (default: stdin)",
    )
    parser.add_argument(
        "--format",
        "-f",
        default="auto",
        choices=["auto", "xml", "binary", "notation"],
        help="LLSD format",
    )
    args = parser.parse_args(argv)

    if args.input is None:
        parser.print_help(file=sys.stderr)
        sys.exit(2)

    input = args.input.read() if isinstance(args.input, BufferedReader) else args.input.encode("utf-8")

    parser = llsd.parse if args.format == "auto" else getattr(llsd, f"parse_{args.format}")

    try:
        print(json.dumps(parser(input), cls=JSONEncoder))
    except llsd.LLSDParseError as e:
        sys.exit(f"LLSD decode error: {e}")


def json2llsd(argv: Iterable[str] = None):
    parser = argparse.ArgumentParser(description="Convert JSON to LLSD")
    parser.add_argument(
        "--format",
        "-f",
        default="xml",
        choices=["xml", "binary", "notation"],
        help="LLSD format",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="JSON string (default: stdin)",
    )
    args = parser.parse_args(argv)

    if args.input is None:
        parser.print_help(file=sys.stderr)
        sys.exit(2)

    input = args.input.read() if isinstance(args.input, TextIOWrapper) else args.input
    try:
        json_obj = json.loads(input)
    except json.JSONDecodeError as e:
        sys.exit(f"JSON decode error: {e}")

    formatter: Callable[[Any], bytes] = getattr(llsd, f"format_{args.format}")

    if args.format == "binary":
        # work around inconsistent header inclusion in llsd library
        formatter = format_binary

    sys.stdout.buffer.write(formatter(json_obj))

