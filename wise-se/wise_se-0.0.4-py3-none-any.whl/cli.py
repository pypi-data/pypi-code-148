import argparse
import sys

# Exit Codes
from antlr4.error.Errors import ParseCancellationException

import wise
from wise.bugfinder import find_bugs, BugFound
from wise.parser import parse_imp
from wise.streams import peek

USAGE_ERROR = 2
DATA_FORMAT_ERROR = 65


def main():
    parser = argparse.ArgumentParser(
        prog="wise",
        description="A Python implementation of the verified symbolic executor WiSE "
        + f"(v{wise.__version__})",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=10,
        help="the number of symbolic states to explore",
    )

    parser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="the IMP file to execute",
    )

    args = parser.parse_args()

    depth = args.depth
    file_name = args.file.name
    file_contents = args.file.read()

    try:
        parsed = parse_imp(file_contents)
    except ParseCancellationException:
        print(f"Error parsing file {file_name}")
        sys.exit(DATA_FORMAT_ERROR)

    print(f"Analyzing file {file_name}\n")

    stream = find_bugs(parsed)
    bug_found = False
    for _ in range(depth):
        next_result = next(stream)
        if isinstance(next_result, BugFound):
            bug_found = True
            print("BUG FOUND")
            (path, store), _ = next_result.s
            print(f"  Path:  {path}")
            print(f"  Store: {store}")

    if not bug_found:
        print(f"No bug found at depth {depth}.")

