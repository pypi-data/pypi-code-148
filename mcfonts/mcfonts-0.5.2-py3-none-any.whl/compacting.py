#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Compacting is the process of taking every "bitmap" character texture provided
by a Minecraft font provider and storing it in as little space as possible.

Generally, this means:

1. Finding the largest effective dimensions out of all the characters,
2. Expanding the dimensions of all other character textures to fit those new dimensions,
3. Creating a new texture that will fit all characters in those dimensions,
4. Sequencing them one-after-another while ignoring characters with a blank texture,
5. Creating a new charlist that corresponds with the compacted texture.

This contains functions for compacting any provider(s) into individual textures
(one for each provider), and for compacting a list of providers into a single, cohesive texture.
"""
import math

import PIL.Image
import mcfonts.utils.bitmap


def compact_providers(
    providers: list[mcfonts.providers.AnyVanillaProvider],
    chars_in_row: int = 0,
    cell_size: tuple[int, int] = (0, 0),
    square_cells: bool = True,
    include_empty_glyphs: bool = True,
) -> tuple[list[str], PIL.Image.Image, tuple[int, int]]:
    """
    Compact the textures and character arrays in `providers`.
    All padding (null, space) will be removed, and blank space will be removed.
    Providers that are not "bitmap" type are ignored.

    This will result in a sheet file with only textured characters.
    This function is different from :func:`compact_providers`,
    in that it will modify the maximum character based on all the providers.

    It returns a single tuple of the new charlist list,
    and the resulting compacted :class:`PIL.Image.Image`.

    :param providers:
        A list of :class:`mcfonts.providers.AnyProvider` instances,
        although only :class:`mcfonts.providers.BitmapProvider` instances will be considered.
    :param chars_in_row: How many characters to fit inside each row of the resulting sheet.
        Only positive values will set fixed rows.
        If this is 0, this will be set to the largest length of the first string in the
        charlist of all providers.
        If this is negative, this will be set so that the resulting sheet is square.
        By default, this is 0 (auto first string).
    :param cell_size:
        What size to make each glyph cell.
        If this is (0, 0), this will be set to the largest dimensions of every glyph in `glyphs`.
        If this is any other tuple of numbers,
    :param square_cells:
        If True, each glyph's width will equal its height.
        This is based on whichever number is largest.
        If False, each glyph's width will be unrelated to its height.
    :param include_empty_glyphs:
        If True, None elements in `glyphs` will be skipped over but their presense will be shown
        in the resulting file (empty space).
        If False, they will be filtered out entirely before being used.
    :returns:
        A list of the new characters, and a tuple containing a modified `resource`
        with the least amount of padding between glyphs,
        plus a tuple of the size of each glyph cell.
    """
    extracted: dict[str, PIL.Image.Image] = {}
    for provider in providers:
        if isinstance(provider, mcfonts.providers.BitmapProvider):
            extracted.update(provider.glyphs)

    if chars_in_row == 0:
        chars_in_row = max(
            len(provider.contents["chars"][0] or "")
            for provider in providers
            if isinstance(provider, mcfonts.providers.BitmapProvider)
        )
    elif chars_in_row < 0:
        chars_in_row = math.ceil(math.sqrt(len(extracted)))

    compacted = compact_glyphs(list(extracted.values()), chars_in_row, cell_size, square_cells, include_empty_glyphs)
    return (
        list(mcfonts.utils.fit_chars_into_charlist(list(extracted.keys()), chars_in_row)),
        compacted[0],
        compacted[1],
    )


def compact_glyphs(
    glyphs: list[PIL.Image.Image | None],
    chars_in_row: int = 0,
    cell_size: tuple[int, int] = (0, 0),
    square_cells: bool = True,
    include_empty_glyphs: bool = True,
) -> tuple[PIL.Image.Image, tuple[int, int]]:
    """
    Given a list of glyphs,
    return an image wherein all glyphs are compacted into a single sheet,
    with the number of glyphs in one row matches ``chars_in_row`` (excluding exceptions).

    :param glyphs: A list of :class:`PIL.Image.Image`.
    :param chars_in_row: How many characters to fit inside each row of the resulting sheet.
        Only positive values will set fixed rows.
        If this is negative or 0, this will be set so that the resulting sheet is square.
        By default, this is 0 (square).
    :param cell_size:
        What size to make each glyph cell.
        If this is (0, 0), this will be set to the largest dimensions of every glyph in `glyphs`.
        If this is any other tuple of numbers,
    :param square_cells:
        If True, each glyph's width will equal its height.
        This is based on whichever number is largest.
        If False, each glyph's width will be unrelated to its height.
    :param include_empty_glyphs:
        If True, None elements in `glyphs` will be skipped over but their presense will be shown
        in the resulting file (empty space).
        If False, they will be filtered out entirely before being used.
    :returns:
        A tuple containing a modified `resource` with the least amount of padding between glyphs,
        plus a tuple of the size of each glyph cell.
    """
    if not include_empty_glyphs:
        glyphs = list(glyph for glyph in glyphs if glyph is not None)
    if chars_in_row <= 0:
        chars_in_row = math.ceil(math.sqrt(len(glyphs)))

    if cell_size == (0, 0):
        max_cell = mcfonts.utils.bitmap.get_largest_effective_glyph_dimensions(glyphs)
    else:
        max_cell = cell_size
    if square_cells:
        maximum = max(max_cell)
        max_cell = (maximum, maximum)

    destination = PIL.Image.new(
        "RGBA",
        (max_cell[0] * chars_in_row, max_cell[1] * len(glyphs) // chars_in_row),
        (0, 0, 0, 0),
    )
    for index, glyph in enumerate(glyphs):
        if glyph:
            destination.paste(
                glyph,
                (
                    (index % chars_in_row) * max_cell[0],
                    (index // chars_in_row) * max_cell[1],
                ),
            )
    return destination, max_cell
