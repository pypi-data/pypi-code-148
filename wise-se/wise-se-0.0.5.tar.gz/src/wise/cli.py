import argparse
import sys

from antlr4.error.Errors import ParseCancellationException

import wise
from wise.bugfinder import find_bugs, BugFound, find_bugs_depth_first
from wise.helpers import is_unsat, simplify_expr
from wise.parser import parse_imp

# Exit Codes
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
        "-n",
        "--nodes",
        type=int,
        default=10,
        help="the number of symbolic states to explore",
    )

    parser.add_argument(
        "-d",
        "--depth-first",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="run symbolic execution in depth-first mode (not as in original WiSE)",
    )

    parser.add_argument(
        "-s",
        "--simplify",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=True,
        help="simplify output path conditions",
    )

    parser.add_argument(
        "--filter-satisfiable",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=True,
        help="remove unsatisfiable potential bugs from the output",
    )

    parser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="the IMP file to execute",
    )

    args = parser.parse_args()

    nodes = args.nodes
    depth_first = args.depth_first
    simplify = args.simplify
    filter_satisfiable = args.filter_satisfiable
    file_name = args.file.name
    file_contents = args.file.read()

    try:
        parsed = parse_imp(file_contents)
    except ParseCancellationException:
        print(f"Error parsing file {file_name}")
        sys.exit(DATA_FORMAT_ERROR)

    print(f"Analyzing file {file_name}\n")

    stream = find_bugs_depth_first(parsed) if depth_first else find_bugs(parsed)

    bug_found = False
    for _ in range(nodes):
        next_result = next(stream)
        if isinstance(next_result, BugFound):
            unsatisfiable = is_unsat(next_result.s[0][0])
            if filter_satisfiable and unsatisfiable:
                continue

            bug_found = True
            print("BUG FOUND" + (" (UNSATISFIABLE)" if unsatisfiable else ""))
            (path, store), _ = next_result.s

            if simplify:
                path = simplify_expr(path)

            print(f"  Path:  {path}")
            print(f"  Store: {store}")

    if not bug_found:
        print(f"No bug found at depth {nodes}.")
