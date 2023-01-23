from __future__ import annotations

import tokenize
from pathlib import Path
from token import COMMENT
from tokenize import TokenInfo
from typing import List


class CodeLine:
    def __init__(self, text: str, hash_col: int | None) -> None:
        self._hash_col = hash_col

        if hash_col is not None:
            self._prefix = text[:hash_col]
            self.comment = text[hash_col + 1 :]
        else:
            self._prefix = text
            self.comment = ""

    @property
    def has_inline_comment(self) -> bool:
        return (self.prefix.strip() != "") and self.comment != ""

    @property
    def has_lone_comment(self) -> bool:
        return (self.prefix.strip() == "") and self.comment != ""

    @property
    def text(self) -> str:
        if self.comment:
            return f"{self.prefix}#{self.comment}"
        return f"{self.prefix}"

    @property
    def hash_col(self) -> int | None:
        return self._hash_col

    @hash_col.setter
    def hash_col(self, new_col: int) -> None:
        assert self._hash_col is not None, "Don't move non-existent comment."
        assert new_col >= self._hash_col, "Don't move comment backward."
        self._prefix += " " * (new_col - self._hash_col)
        self._hash_col = new_col

    @property
    def prefix(self) -> str:
        return self._prefix

    def __repr__(self) -> str:
        return self.__class__.__qualname__ + f"({self.text!r})"


# TODO: I don't think this class is really useful anymore.
class CodeLines(List[CodeLine]):
    def __init__(self, path: Path | str):
        self.path = Path(path)

        with tokenize.open(path) as fh:
            tokens = tokenize.generate_tokens(fh.readline)

            comment_token: TokenInfo | None = None
            for token in tokens:
                if token.type == COMMENT:
                    comment_token = token
                elif token.string == "\n":
                    comment_col = comment_token.start[1] if comment_token else None
                    self.append(CodeLine(token.line, comment_col))
                    comment_token = None


def main() -> None:
    path = Path(__file__).parent.parent.parent / "tests" / "examples" / "align_bad.py"
    code_lines = CodeLines(path)
    print("all lines:", *code_lines, sep="\n")


if __name__ == "__main__":
    main()
