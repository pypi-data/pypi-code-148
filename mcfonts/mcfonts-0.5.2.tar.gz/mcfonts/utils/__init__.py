#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Utilities for Minecraft fonts. Not all of these are used.
"""
import os
import re
import typing

import PIL.Image
import mcfonts.colors
import mcfonts.constants
import mcfonts.utils.unicode


def resolve_resource_path(path: str, json_path: str, subpath: str = "") -> str:
    """
    Resolve the correct path to the resource indicated by ``path``,
    using ``json_path`` as the base path to follow from.
    ``json_path`` is the font's JSON path, ``path`` is the request resource path.

    >>> mcfonts.utils.resolve_resource_path("mypath", "mypath/font.json", "textures")
    '~/mcfonts/textures/mypath'

    :param path: Unresolved path to the resource.
    :param json_path: Path to the font JSON.
    :param subpath: Resource will be loaded from the ``subpath`` directory.
    :returns: An absolute path of the request resource, ``path``.
    """
    temppath = path.split(":", 1)
    if len(temppath) > 1:
        # Uses a namespace
        return expand_path(
            os.path.join(
                json_path,
                f"../../../{temppath[0]}/{subpath}/{temppath[1]}",
            )
        )
    return expand_path(os.path.join(json_path, f"../../{subpath}/{temppath[0]}"))


def sanitize_font_name(font_name: str) -> str:
    """
    Ensure ``sanitized_font_name`` is a valid PostScript font name.
    A PostScript font name cannot:

    * Contain ``(){}[]<;>%/`` or space
    * Be longer than 63 characters
    * Have non-ASCII characters

    >>> mcfonts.utils.sanitize_font_name("\u2600 This is a really long name!")
    '_This_is_a_really_long_name!'

    :param font_name: The font name to sanitize.
    :returns: A valid PostScript font name.
    """
    return re.sub(r"[{}\[\]() <>%/]", "_", font_name)[:63].encode("ascii", "ignore").decode("ascii")


def expand_path(path: str) -> str:
    """
    Expand ``path`` with any variables or shortcuts, such as ``~``, ``$HOME``, etc.

    >>> mcfonts.utils.expand_path("~/Documents")
    '/home/me/Documents'

    :param path: The unexpanded path.
    :returns: The expanded absolute path.
    """
    return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))


def expand_resource_location(file_path: str) -> str:
    """
    Take any path to a texture file and return the Minecraft file string for it.

    :param file_path: A fully-expanded path to any file.
    :returns: A string in the format of "<namespace>?:<dir/>?<file>".
    """
    splitted = re.split(f"[{os.path.sep}:]", file_path)
    try:
        assets = splitted.index("assets")
    except ValueError:
        assets = -1
    if (namespace := splitted[0]) == "minecraft":
        return f"{splitted[assets + 3]}/{'/'.join(splitted[assets + 4:])}"
    return f"{namespace}/{splitted[assets + 3]}/{'/'.join(splitted[assets + 4:])}"


def fit_chars_into_charlist(chars: list[str], charlist_length: int = 16) -> typing.Iterator[str]:
    """
    Given a list of chars, fit them into a charlist whose width is equal to `charlist_length`.

    >>> list(mcfonts.utils.fit_chars_into_charlist(["thisisareallylongcharlist"]))
    ['thisisareallylon', 'gcharlist']
    >>> list(mcfonts.utils.fit_chars_into_charlist(["thisisareallylongcharlist"], 5))
    ['thisi', 'sarea', 'llylo', 'ngcha', 'rlist']

    :param chars: A list of chars.
    :param charlist_length: The width to make each line of characters in the charlist equal to.
    :returns: Yield of lines in a charlist.
    """
    chars = list(mcfonts.utils.charlist_to_chars(chars))
    for i in range(0, len(chars), charlist_length):
        yield "".join(char for char in chars[i : i + charlist_length])


def charlist_to_chars(charlist: list[str]) -> typing.Iterator[str]:
    """
    Given `charlist`, yield all the characters that charlist covers.

    >>> chars = ['agtg', 'b', '5', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8']
    >>> list(mcfonts.utils.charlist_to_chars(chars)
    ['a', 'g', 't', 'g', 'b', '5', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8']

    :param charlist: The charlist.
    :returns: A yield of characters.
    """
    for charline in charlist:
        # iterating over lines, charline is a string
        for character in charline:
            # iterating over chars, char is a str[1]
            yield character


def is_image_empty(image: PIL.Image.Image) -> bool:
    """
    Determine if `image` has any pixel data.

    :param image: A :class:`PIL.Image.Image`.
    :returns: If `image` has pixel data.
    """
    extrema = image.getextrema()
    if isinstance(extrema[0], int):
        return extrema[0] == 0 and extrema[1] == 0
    for band in extrema:
        if band[0] != 0 or band[1] != 0:
            return False
    return True


def is_image_invisible(image: PIL.Image.Image) -> bool:
    """
    Determine if `image` has all invisible pixels; if alpha is 0.

    :param image: A :class:`PIL.Image.Image`.
    :returns: If `image` doesn't have any full-alpha pixels.
    """
    if image.mode == "RGBA":
        return all(pixel == 0 for pixel in image.getdata(3))
    if image.mode == "LA":
        return all(pixel == 0 for pixel in image.getdata(1))
    return False


def is_charline_empty(charline: str) -> bool:
    r"""
    Given `charline`, return if it contains only spaces or null bytes.

    >>> mcfonts.utils.is_charline_empty("\0\0\0\x20\x20\x20\0\0")
    True

    >>> mcfonts.utils.is_charline_empty("         ")
    True

    >>> mcfonts.utils.is_charline_empty("      xxx")
    False

    :param charline: A single string, likely part_notation of a wider charlist.
    :returns: If `charline` is all spaces or null bytes.
    """
    return all(x in mcfonts.constants.PADDING_CHARS for x in charline)


def color_number(number: float | int) -> str:
    """
    Given `number`, return a colorized and pretty-print version of that number.

    .. note::
        If :data:`mcfonts.colors.USE_COLORS` is False, color will not be applied.

    If `number` is negative, it will be in red.
    If `number` is positive, it will be in green.
    If `number` is zero, it will have no colors.

    :param number: The number, positive or negative.
    :returns: A string representing `number` with color codes.
    """
    if number < 0:
        if mcfonts.colors.USE_COLORS:
            return f"{mcfonts.colors.RED_FORE}{number:,}{mcfonts.colors.RESET_FORE}"
        return f"{number:,}"
    if number == 0:
        return f"{number:,}"
    if mcfonts.colors.USE_COLORS:
        return f"{mcfonts.colors.GREEN_FORE}+{number:,}{mcfonts.colors.RESET_FORE}"
    return f"+{number:,}"
