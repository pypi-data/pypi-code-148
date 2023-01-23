from __future__ import annotations

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path

import comform
from comform.codeline import CodeLines
from comform.fixers import fix_align, fix_blocks, fix_dividers


def get_parser() -> ArgumentParser:

    parser = ArgumentParser(
        prog="comform",
        description="Python Comment Conformity Formatter",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        help="print the version number",
        version=comform.__version__,
    )
    # TODO: check really doesn't do anything atm
    parser.add_argument(
        "--check", "-c", action="store_true", help="do not write to files."
    )
    parser.add_argument(
        "--align", "-a", action="store_true", help="align in-line comments"
    )
    parser.add_argument(
        "--dividers", "-d", action="store_true", help="correct section divider comments"
    )
    parser.add_argument(
        "--wrap",
        "-w",
        default=88,
        type=int,
        help="Column at which to wrap comments",
        metavar="N",
    )
    parser.add_argument(
        "paths", nargs="+", help="folders/files to re-format (recursively)"
    )

    return parser


def run(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    options = get_parser().parse_args(args)

    align = options.align
    dividers = options.dividers
    wrap = options.wrap
    check = options.check

    altered = []
    for path_name in options.paths:
        path = Path(path_name)
        file_paths = path.glob("**/*.py") if path.is_dir() else [path]

        for file in file_paths:
            # TODO: don't open file twice:
            with open(file, encoding="utf8") as fh:
                original = fh.read()
            code_lines = CodeLines(file)

            if align:
                fix_align(code_lines)
            if dividers:
                fix_dividers(code_lines, col_max=wrap)
            fix_blocks(code_lines, col_max=wrap)
            result = "".join(line.text for line in code_lines)

            if result == original:
                continue

            altered.append(file)
            if not check:
                with open(file, "w", encoding="utf8") as fh:
                    fh.write(result)

        header = "Failed files:" if check else "Altered Files:"
        print(header, *(altered if altered else ["\b(None)"]), sep="\n")  # type: ignore[list-item]
