from __future__ import annotations

import typing as t

from slugify import slugify


__all__ = ("type_slug", )


def type_slug(
    value: str,
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
) -> str:
    """A slug is a short label for something, containing only letters, numbers,
    underscores or hyphens.

    Uses `python-slugify` to do the conversion so it takes the same arguments:

        max_length (int):
            output string length

        separator (str):
            separator between words

        stopwords:
            list of words to discount

        regex_pattern (str):
            regex pattern for allowed characters

        replacements:
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
    return slugify(
        value or "",
        max_length=max_length,
        separator=separator,
        stopwords=stopwords or [],
        regex_pattern=regex_pattern,
        replacements=replacements or [],
        lowercase=lowercase,
        word_boundary=word_boundary,
        entities=entities,
        decimal=decimal,
        hexadecimal=hexadecimal
    )
