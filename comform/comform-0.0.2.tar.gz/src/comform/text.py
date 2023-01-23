"""Wrapper around `mdformat`."""
from __future__ import annotations

from typing import Literal

import mdformat


def format_as_md(
    text: str,
    /,
    *,
    wrap: int | Literal["keep", "no"] = "keep",
    number: bool = False,
    eol: Literal["lf", "crlf", "keep"] = "lf",
) -> str:
    options = {"wrap": wrap, "number": number, "end-of-line": eol}
    return mdformat.text(text, options=options)
