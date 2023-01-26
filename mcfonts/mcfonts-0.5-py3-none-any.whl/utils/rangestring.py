#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Utilities for constructing and translating rangestrings.
See :doc:`rangestrings` for details on the syntax.
"""
import mcfonts.constants
import mcfonts.exceptions


def part_to_character(part_notation: str) -> str:
    """
    Given a part of a rangestring, return the character it translates to.

    For details on what this notation should be, see :doc:`/rangestrings`.
    This notation should match this regular expression
    :const:`mcfonts.constants.RANGESTRING_PART`.

    >>> part_to_character("U+2600")
    '☀'
    >>> part_to_character("0x2541")
    '╁'

    :param part_notation: A rangestring part.
    :returns: A single character.
    :raises mcfonts.exceptions.RangestringError: If the part is not valid.
    """
    if parts := mcfonts.constants.RANGESTRING_PART.fullmatch(part_notation):
        if (single_char := parts.group(5)) is not None:
            return single_char
        return chr(int(parts.group(4), 16))
    raise mcfonts.exceptions.RangestringError("Invalid part in rangestring")


def range_to_update(range_notation: str, current_coverage: set[str] | None = None) -> None:
    """
    Given a range of a rangestring, update `current_coverage` with the characters it translates to.

    For details on what this notation should be, see :doc:`rangestrings`.
    This notation should match this regular expression
    :const:`mcfonts.constants.RANGESTRING_RANGE`.

    :param range_notation:
        A rangestring range.
        This function does not accept individual parts.
    :param current_coverage:
        A set of the already-included characters.
        This is required for applying exclusion.
    :returns: Nothing, ``current_coverage`` is updated in place.
    :raises mcfonts.exceptions.RangestringError:
        If the range is not valid,
        or if a single part is supplied instead.
    """
    if current_coverage is None:
        current_coverage = set()
    split = mcfonts.constants.RANGESTRING_RANGE_DELIMITER.split(range_notation, 1)
    len_split = len(split)
    if len_split == 3:
        complete = set(
            chr(i)
            for i in range(
                ord(part_to_character(split[0])),
                # + 1 to be inclusive of last codepoint
                ord(part_to_character(split[2])) + 1,
            )
        )
        if split[0].startswith("!") or split[1].startswith("!"):
            # This is an exclusion, remove it
            current_coverage.difference(complete)
        else:
            current_coverage.update(complete)
    elif len_split == 2:
        raise mcfonts.exceptions.RangestringError(
            f"Implied infinite expansion is not allowed in rangestrings: {range_notation}"
        )
    else:
        raise mcfonts.exceptions.RangestringError(f"Invalid rangestring notation: {range_notation}")


def rangestring_to_characters(rangestring: str) -> set[str]:
    r"""
    Return a set of characters that corresponds to `rangestring`.

    See :doc:`rangestrings` for more details.

    >>> rangestring_to_characters("U+2600..U+26ff,U+1ab0..0x1abf, 0x156, A")
    [['Ŗ', 'A'], range(9728, 9984), range(6832, 6848)]

    :param rangestring: A rangestring.
    :returns: A set of characters.
    """
    current_coverage: set[str] = set()
    for component in mcfonts.constants.RANGESTRING_COMPONENT_DELIMITER.split(rangestring):
        if mcfonts.constants.RANGESTRING_RANGE.fullmatch(component):
            # It's a range
            range_to_update(component, current_coverage)
        elif mcfonts.constants.RANGESTRING_PART.fullmatch(component):
            # It's a part
            if component.startswith("!"):
                # This is an exclusion, remove it
                current_coverage.difference_update(part_to_character(component))
            else:
                current_coverage.update(part_to_character(component))
        elif mcfonts.constants.RANGESTRING_RANGE_DELIMITER.search(component):
            # We didn't match the full range notation but there's a range delimiter in here
            # assume it's A- or -A notation; raise error.
            raise mcfonts.exceptions.RangestringError(
                f"Implied infinite expansion is not allowed in rangestrings: {component}"
            )
        else:
            # It's neither, ???
            raise mcfonts.exceptions.RangestringError(f"Invalid rangestring notation: {component}")
    return current_coverage
