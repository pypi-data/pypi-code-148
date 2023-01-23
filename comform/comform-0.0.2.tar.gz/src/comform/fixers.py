from __future__ import annotations

import re
from pathlib import Path

from comform.codeline import CodeLine, CodeLines
from comform.text import format_as_md


def fix_align(code_lines: CodeLines) -> None:

    batch: list[CodeLine] = []
    for code_line in code_lines:
        if code_line.has_inline_comment:
            batch.append(code_line)
        elif batch:
            max_hash_col = max(line.hash_col for line in batch)  # type: ignore[type-var]
            for commented_code in batch:
                commented_code.hash_col = max_hash_col
            batch = []


def fix_blocks(code_lines: CodeLines, /, col_max: int) -> None:

    block: list[CodeLine] = []
    row = 0
    while row < len(code_lines):
        code_line = code_lines[row]

        # TODO: fails to consider the case of:
        # ```python
        # # blah blah
        #       # blah blah
        # ```
        if code_line.has_lone_comment:
            if not block:
                batch_start_row = row
            block.append(code_line)
        elif block:
            col = block[0].hash_col
            assert col is not None
            wrap = col_max - col - len("# ")

            text = "".join(line.comment for line in block)
            text = format_as_md(text, number=True, wrap=wrap).strip()
            new_lines = [
                CodeLine(" " * col + f"# {line}\n", col)
                if line
                else CodeLine(" " * col + "#\n", col)
                for line in text.split("\n")
            ]

            code_lines[batch_start_row : batch_start_row + len(block)] = new_lines
            row = batch_start_row + len(new_lines)
            block = []

        # TODO: check this doesn't sometimes cause an off-by-one error
        row += 1


def fix_dividers(code_lines: CodeLines, /, col_max: int) -> None:

    for line in code_lines:
        match = re.match(r" *-+([^-]+)-+ *#?", line.comment)
        if match:
            text = format_as_md(match.group(1), wrap="no").strip()
            dashes = "-" * (col_max - len(text) - len(" -- " + " " + " #\n"))
            line.comment = f" -- {text} {dashes} #\n"


def run_all(filename: str | Path, col_max: int = 88) -> str:

    code_lines = CodeLines(filename)

    fix_blocks(code_lines, col_max)
    fix_dividers(code_lines, col_max)
    fix_align(code_lines)

    return "".join(line.text for line in code_lines)
