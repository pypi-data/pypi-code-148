#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Utilities for the "legacy_unicode" font provider.
Most of these are for either handling codepages, or for building template chars.
"""

import os

import PIL.Image
import mcfonts.constants
import mcfonts.utils.bitmap


def build_template_for_char(char: str, path_to_template_textures: str | None = None) -> PIL.Image.Image:
    """
    Build an image of a template :term:`codepoint`.
    Templates are simple white boxes with a codepoint :term:`texture` inside them.
    This is intended for use with a "legacy_unicode" :term:`provider`.

    :param char:
        A single character.
        This character's codepoint is what goes inside the box.
    :param path_to_template_textures:
        The path to the folder that contains the digit textures.
        See the documentation for :func:`mcfonts.templates.generate_unicode_template_font`.
    :returns: A :class:`PIL.Image.Image` of the char template
    """
    codepoint = ord(char)
    templates = generate_unicode_template_font(path_to_template_textures)
    if codepoint > 0xFFFF:
        box = templates[-6]
        # 0xABCDEF -> A
        box.paste(templates[(codepoint & 0xF00000) >> 20], (2, 2))
        # 0xABCDEF -> B
        box.paste(templates[(codepoint & 0xF0000) >> 16], (6, 2))
        # 0xABCDEF -> C
        box.paste(templates[(codepoint & 0xF000) >> 12], (10, 2))
        # 0xABCDEF -> D
        box.paste(templates[(codepoint & 0xF00) >> 8], (2, 9))
        # 0xABCDEF -> E
        box.paste(templates[(codepoint & 0xF0) >> 4], (6, 9))
        # 0xABCDEF -> F
        box.paste(templates[(codepoint & 0xF)], (10, 9))
    else:
        box = templates[-4]
        # 0xABCD -> A
        box.paste(templates[(codepoint & 0xF000) >> 12], (2, 2))
        # 0xABCD -> B
        box.paste(templates[(codepoint & 0xF00) >> 8], (6, 2))
        # 0xABCD -> C
        box.paste(templates[(codepoint & 0xF0) >> 4], (2, 9))
        # 0xABCD -> D
        box.paste(templates[codepoint & 0xF], (6, 9))
    return box


def generate_unicode_template_font(path: str | None = None) -> dict[int, PIL.Image.Image]:
    """
    Generate a dictionary of hex -> sheet.

    Path must point to a folder where these files exist (PNG format):

    * <0-9>.png
    * <a-f>.png
    * box4.png
    * box6.png

    The file names **are** case-sensitive
    and the textures for hex charlist **must** be 3 pixels wide by 6 pixels tall.

    The sheet for "box6.png" must be 16 x 16 pixels.
    The sheet for "box4.png" must be 12 x 16 pixels.
    Hex charlist are overlayed atop the box.

    Box4 is for chars below 0x10000 (4 points, F4E -> 0F4E; 4).
    Box6 is for chars above 0xFFFF (6 points, 1FAE6 -> 01FAE6; 6).

    Color does not matter.

    This is used for generating Unicode template characters,
    see :func:`mcfonts.utils.legacy_unicode.build_template_for_char`.

    :param path:
        Path to the folder where these textures exist.
        If this is falsy (None, ""), the path will be set automatically from the module and will
        use pre-made character textures that were distributed with this module.
    :returns:
        A dictionary that maps 0-15 to a glyph.
        -4 and -6 are box4 and box6, respectively.
    """
    if path:
        templates = mcfonts.utils.expand_path(path)
    else:
        templates = mcfonts.utils.expand_path(os.path.join(__file__, "../../template_hexchar_textures"))
    return {
        0: PIL.Image.open(f"{templates}/0.png"),
        1: PIL.Image.open(f"{templates}/1.png"),
        2: PIL.Image.open(f"{templates}/2.png"),
        3: PIL.Image.open(f"{templates}/3.png"),
        4: PIL.Image.open(f"{templates}/4.png"),
        5: PIL.Image.open(f"{templates}/5.png"),
        6: PIL.Image.open(f"{templates}/6.png"),
        7: PIL.Image.open(f"{templates}/7.png"),
        8: PIL.Image.open(f"{templates}/8.png"),
        9: PIL.Image.open(f"{templates}/9.png"),
        10: PIL.Image.open(f"{templates}/a.png"),
        11: PIL.Image.open(f"{templates}/b.png"),
        12: PIL.Image.open(f"{templates}/c.png"),
        13: PIL.Image.open(f"{templates}/d.png"),
        14: PIL.Image.open(f"{templates}/e.png"),
        15: PIL.Image.open(f"{templates}/f.png"),
        -4: PIL.Image.open(f"{templates}/box4.png"),
        -6: PIL.Image.open(f"{templates}/box6.png"),
    }


def align_unicode_page(sheet: PIL.Image.Image) -> PIL.Image.Image:
    """
    Align a Unicode page font sheet's characters to the left.

    This function is really a shortcut for
    ``mcfonts.utils.bitmap.align_font_texture(sheet, (16, 16))``.

    :param sheet: The font sheet, not the individual character.
    :returns: The new font sheet.
    """
    return mcfonts.utils.bitmap.align_font_texture(sheet, (16, 16))
