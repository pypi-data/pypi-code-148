from __future__ import annotations

import typing as t

from .text import Text
from ..ftypes import type_slug


__all__ = ("Slug",)


class Slug(Text):
    """A slug is a short label for something, containing only letters, numbers,
    underscores or hyphens.

    Uses [python-slugify](https://github.com/un33k/python-slugify) library to do the
    conversion so it takes the same arguments:

        max_length (int):
            output string length

        separator (str):
            separator between words

        stopwords (list):
            words to discount

        regex_pattern (str):
            regex pattern for allowed characters

        replacements (list):
            list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]

        lowercase (bool):
            activate case sensitivity by setting it to False

        word_boundary (bool):
            truncates to end of full words (length may be shorter than max_length)

        entities (bool):
            converts html entities to unicode (foo &amp; bar -> foo-bar)

        decimal (bool):
            converts html decimal to unicode (&#381; -> Ž -> z)

        hexadecimal (bool):
            converts html hexadecimal to unicode (&#x17D; -> Ž -> z)

    """

    def __init__(
        self,
        *validators,
        max_length: int = 0,
        separator: str = "-",
        stopwords: t.Iterable[str] | None = None,
        regex_pattern: str | None = None,
        replacements: t.Iterable[str] | None = None,
        lowercase: bool = True,
        word_boundary: bool = False,
        entities: bool = True,
        decimal: bool = True,
        hexadecimal: bool = True,
        **kwargs
    ):
        super().__init__(
            *validators,
            max_length=max_length or 0,
            separator=separator,
            stopwords=stopwords,
            regex_pattern=regex_pattern,
            replacements=replacements,
            lowercase=lowercase,
            word_boundary=word_boundary,
            entities=entities,
            decimal=decimal,
            hexadecimal=hexadecimal,
            **kwargs
        )

    def type(self, value: str, **options) -> str:
        return type_slug(value, **options)
