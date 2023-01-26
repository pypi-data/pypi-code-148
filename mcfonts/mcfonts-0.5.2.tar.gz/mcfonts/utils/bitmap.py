#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Utilities for the "bitmap" font provider.
Most of these are for either aligning sheets, getting glyphs, or padding charlists.
"""
import itertools
import typing

import PIL.Image
import PIL.ImageChops

import mcfonts.constants
import mcfonts.utils.exporting
import mcfonts.providers
import mcfonts.utils.unicode


def pad_charlist(
    charlist: list[str],
    pad_amount: int = 0,
    pad_char: str = " ",
    pad_from: typing.Literal["left", "right"] = "right",
) -> list[str]:
    """
    Pad `charlist` so that all of its strings have the same length.

    :param charlist: Character list to pad.
    :param pad_amount: What to pad the characters to; the ideal width.
        If this is 0, this will be determined from the largest length of strings in `charlist`.
    :param pad_char: The character to pad with, default is a space.
    :param pad_from: Direction to pad the string from, left => "___Text", right => "Text___".
    :returns: The padded charlist list.
    """
    if pad_from not in ("left", "right"):
        raise ValueError('pad_from must be "left" or "right"')
    if pad_amount == 0:
        # Get the largest string based on length
        pad_amount = len(max(charlist, key=len))
    for index, charline in enumerate(charlist):
        if len(charline) != pad_amount:
            if pad_from == "left":
                # Rjust means justify to right
                charlist[index] = charline.rjust(pad_amount, pad_char[0])
            else:
                # Ljust means justify to left
                charlist[index] = charline.ljust(pad_amount, pad_char[0])
    return charlist


def assert_charlist_is_equal(charlist: list[str]) -> tuple[bool, int]:
    """
    Ensure that every string inside `charlist` has the same length as the first string.

    :param charlist: The charlist of strings to check lengths of.
    :returns: A tuple of (if the lengths are equal, the expected length).
    """
    ideal = len(max(charlist, key=len))
    for charline in charlist:
        if len(charline) != ideal:
            return False, ideal
    return True, ideal


def align_font_texture(
    sheet: PIL.Image.Image, glyph_cell: tuple[int, int] = (8, 8), new_left_padding: int = 0
) -> PIL.Image.Image:
    """
    Align a font sheet's character's sheet in order to what `new_left_padding` is.

    This only shifts the character on the X axis (horizontally, left-right).

    :param sheet: The font sheet, not the individual glyph.
    :param glyph_cell: The dimensions of each individual character, their cell bounding box.
    :param new_left_padding: The distance away from the left edge the new character should be.
    :returns: The new font sheet.
    """
    height = sheet.height // glyph_cell[1]
    width = sheet.width // glyph_cell[0]
    for y_position in range(height):
        for x_position in range(width):
            # Glyph dimensions before alignment
            dimensions = (
                x_position * glyph_cell[0],
                y_position * glyph_cell[1],
                (x_position + 1) * glyph_cell[0],
                (y_position + 1) * glyph_cell[1],
            )
            # Get the glyph itself
            glyph = sheet.crop(dimensions)
            # If width is not the new padding, offset it by the difference
            if (margin := mcfonts.utils.exporting.get_glyph_nominals(glyph)[0]) != new_left_padding:
                sheet.paste(PIL.ImageChops.offset(glyph, new_left_padding - margin, 0))
    return sheet


def get_largest_effective_glyph_dimensions(
    glyphs: list[PIL.Image.Image | None], isolate_dimensions: bool = True
) -> tuple[int, int]:
    """
    Given a :class:`collections.deque` of glyphs,
    return the width and height of the largest character in that deque.

    This function operates based on the actual pixels inside an image; it crops out empty space
    and then determines the width and height. For a function that operates on an image's true
    width and height, see :func:`get_largest_glyph_dimensions`.

    :param glyphs: A deque of the glyphs to iterate over.
    :param isolate_dimensions:
        If True, the maximum height and width will be calculated separately.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 9).
        If False, the maximum height and width is dependent on the maximum width found.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 8).
        It is recommended that you leave this to True.
    :returns: A tuple of (maximum width, maximum height).
    """
    max_width = 0
    max_height = 0
    for glyph in glyphs:
        if glyph:
            if bbox := glyph.getbbox():
                if (width := bbox[2] - bbox[0]) > max_width:
                    max_width = width
                    if not isolate_dimensions:
                        max_height = width
                    continue
                if (height := bbox[3] - bbox[1]) > max_height:
                    max_height = height
    return max_width, max_height


def get_largest_glyph_dimensions(
    glyphs: list[PIL.Image.Image | None], isolate_dimensions: bool = True
) -> tuple[int, int]:
    """
    Given a :class:`collections.deque` of glyphs,
    return the width and height of the largest character in that deque.

    This function is different from :func:`get_largest_effective_glyph_dimensions` in that it
    does not calculate the real width and height that pixels in an image extend to. It only
    relies on the width and height of the *canvas* of the image.

    :param glyphs: A deque of the glyphs to iterate over.
    :param isolate_dimensions:
        If True, the maximum height and width will be calculated separately.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 9).

        If False, the maximum height and width is dependent on the maximum width found.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 8).

        It is recommended that you leave this to True.
    :returns: A tuple of (maximum width, maximum height).
    """
    max_width = 0
    max_height = 0
    for glyph in glyphs:
        if glyph:
            if glyph.getbbox():
                if (width := glyph.width) > max_width:
                    max_width = width
                    if not isolate_dimensions:
                        max_height = width
                    continue
                if (height := glyph.height) > max_height:
                    max_height = height
    return max_width, max_height


def resource_to_glyphs(
    resource: PIL.Image.Image, char_counts: tuple[int, int]
) -> typing.Iterator[PIL.Image.Image | None]:
    """
    Given a resource and number of characters in each row and column of that resource,
    yield every :class:`PIL.Image.Image` in that resource.

    If no data exists at a cell, yield None.

    :param resource: A :class:`PIL.Image.Image` of the font resource.
    :param char_counts: A tuple of the number of characters in each row and column.
    :returns: A yield of :class:`PIL.Image.Image` glyphs, or None.
    """
    height = resource.height // char_counts[1]
    width = resource.width // char_counts[0]
    for y_index in range(char_counts[1]):
        for x_index in range(char_counts[0]):
            if mcfonts.utils.is_image_empty(
                glyph := resource.crop(
                    (
                        x_index * width,
                        y_index * height,
                        (x_index + 1) * width,
                        (y_index + 1) * height,
                    )
                )
            ):
                yield None
            else:
                yield glyph


def resource_to_charlist(resource: PIL.Image.Image, char: str, cell_bound: tuple[int, int] = (8, 8)) -> list[str]:
    """
    Given a path to a resource and a starting character, return an appropriate charlist.

    Return a provider that has a charlist that correctly encompasses all chars covered by
    the resource. Glyphs in the resource that are empty are skipped over.

    :param resource: The resource to grab textures from.
    :param char:
        A single character.
        The codepoint of this will increase by 1 on every glyph.
    :param cell_bound:
        The dimensions of an individual glyph in `resource`.
        Glyph dimensions must be the same throughout the whole of `resource`.
    :returns: A `chars` list.
    """
    charlist: list[str] = []
    charline: list[str] = []
    codepoint = ord(char)
    for height_offset in range(resource.height // cell_bound[1]):
        for width_offset in range(resource.width // cell_bound[0]):
            if mcfonts.utils.is_image_empty(
                resource.crop(
                    (
                        width_offset * cell_bound[0],
                        height_offset * cell_bound[1],
                        (width_offset + 1) * cell_bound[0],
                        (height_offset + 1) * cell_bound[1],
                    )
                )
            ):
                charline.append(" ")
            else:
                charline.append(chr(codepoint))
            codepoint += 1
        charlist.append("".join(charline))
        charline.clear()
    return charlist


def load_resources(
    providers: list[dict],
    json_path: str,
    strict: bool = False,
    mode: str = "LA",
) -> dict[str, PIL.Image.Image | bytes]:
    """
    Look through every provider and load their source files into a dictionary.

    :param providers: A list of the providers to get resources from.
    :param json_path: The path to the original font JSON.
    :param strict:
        If True:
        * Missing files will raise an error

        If False:
        * Missing files will be skipped

    :param mode: Mode to load the images in. See PIL modes.
    :returns: The loaded resources.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    resources: dict[str, PIL.Image.Image | bytes] = {}
    for provider in providers:
        try:
            if (provider_type := provider.get("type", "")).lower().strip() == "bitmap":
                file = provider.get("file", "")
                resources[file] = load_resources_bitmap(file, json_path).convert(mode)
            elif provider_type == "legacy_unicode":
                resources |= dict(
                    load_resources_legacy_unicode(provider.get("template", ""), json_path, provider.get("sizes", ""))
                )
            elif provider_type == "ttf":
                file = provider.get("file", "")
                resources[file] = load_resources_ttf(file, json_path)
        except PIL.UnidentifiedImageError:
            mcfonts.logger.warning(
                mcfonts.providers.format_provider_message(provider, "has invalid file; must be PNG.")
            )
            continue
        except FileNotFoundError as exception:
            if not strict:
                # Missing files are ignored
                mcfonts.logger.warning(
                    mcfonts.providers.format_provider_message(
                        provider, f'file "{exception.filename}" does not exist, skipping.'
                    )
                )
                continue
            # Missing files not allowed, raising exception
            raise exception
    return resources


def load_resources_bitmap(file_name: str, json_path: str) -> PIL.Image.Image:
    """
    A convenient companion function to :func:`load_resources`,
    but specialized for "bitmap" provider resources.

    :param file_name: The name of the file to search for.
    :param json_path: The path that the original font JSON was located in.
    :return: A :class:`PIL.Image.Image` instance.
    """
    with open(
        mcfonts.utils.resolve_resource_path(file_name, json_path, "textures"),
        "rb",
    ) as open_tempfile:
        image = PIL.Image.open(open_tempfile, formats=["png"])
        image.load()
        return image


def load_resources_legacy_unicode(
    template: str, json_path: str, sizes: str
) -> typing.Iterator[tuple[str, PIL.Image.Image | bytes]]:
    """
    A convenient companion function to :func:`load_resources`,
    but specialized for "legacy_unicode" provider resources.

    :param template: The template string, must include "%s".
    :param json_path: The path that the original font JSON was located in.
    :param sizes: The name of the "sizes" file.
    :returns: A yield of {filename: image}.
    """
    template_parts: list[str] = template.split("%s", 1)
    # Skip surrogates
    for codepage in itertools.chain(range(0xD8), range(0xE0, 0x100)):
        template_name = f"{template_parts[0]}{codepage:02x}{template_parts[1]}"
        try:
            with open(
                mcfonts.utils.resolve_resource_path(template_name, json_path, "font"),
                "rb",
            ) as open_tempfile:
                image = PIL.Image.open(open_tempfile, formats=["png"])
                image.load()
                yield template_name, image
        except FileNotFoundError:
            # Page doesn't exist, acceptable error
            continue
    with open(
        mcfonts.utils.resolve_resource_path(sizes, json_path),
        "rb",
    ) as open_tempfile:
        yield sizes, open_tempfile.read()


def load_resources_ttf(file_name: str, json_path: str) -> bytes:
    """
    A convenient companion function to :func:`load_resources`,
    but specialized for "ttf" provider resources.

    :param file_name: The name of the TTF file to search for.
    :param json_path: The path that the original font JSON was located in.
    :return: Bytes of the TTF file.
    """
    with open(
        mcfonts.utils.resolve_resource_path(file_name, json_path, "font"),
        "rb",
    ) as open_tempfile:
        return open_tempfile.read()


def validate_charlist(
    charlist: list[str],
    resource: PIL.Image.Image | None = None,
    glyph_cell: tuple[int, int] = (8, 8),
):
    """
    Given `charlist`, ensure that it is valid and does not have any possible issues.
    Issues include:

    * Empty lines
    * Uneven lines
    * Duplicate characters
    * \\*Padding chars in places where glyph exists in `resource`
    * \\*Characters that will have an empty glyph in `resource`

    \\* Optional, requires `resource`.

    :param charlist: A charlist to validate.
    :param resource: An optional :class:`PIL.Image.Image` to validate glyph textures against.
    :param glyph_cell: Tuple of (glyph width, glyph height) for each glyph in `resource`.
    """
    char_traces: dict[str, tuple[int, int]] = {}
    for y_index, charline in enumerate(charlist):
        if not (len_charline := len(charline)):
            mcfonts.logger.warning(f"Charline {y_index} is empty.")
        elif not (charlist_length := mcfonts.utils.bitmap.assert_charlist_is_equal(charlist))[0]:
            mcfonts.logger.warning(
                "Uneven amount of characters in charlist,"
                f"expected {charlist_length[1]}, got {len_charline} on line {y_index}.",
            )
        for x_index, character in enumerate(charline):
            if character not in mcfonts.constants.PADDING_CHARS and character in char_traces:
                trace = char_traces[character]
                mcfonts.logger.warning(
                    f"Duplicate character {mcfonts.utils.unicode.pretty_print_char(character)} "
                    f"on charline {y_index} index {x_index}. "
                    f"Character was already defined at charline {trace[0]} index {trace[1]}.",
                )
            else:
                char_traces[character] = (y_index, x_index)
            if resource:
                is_glyph_invisible = mcfonts.utils.is_image_invisible(
                    resource.crop(
                        (
                            x_index * glyph_cell[0],
                            y_index * glyph_cell[1],
                            (x_index + 1) * glyph_cell[0],
                            (y_index + 1) * glyph_cell[1],
                        )
                    )
                )
                if not is_glyph_invisible and character in mcfonts.constants.PADDING_CHARS:
                    mcfonts.logger.debug(
                        f"Padding character on charline {y_index} index {x_index}, but glyph data exists.",
                    )
                elif is_glyph_invisible and not mcfonts.utils.unicode.is_char_invisible(character):
                    mcfonts.logger.debug(
                        "Empty glyph for character "
                        f"{mcfonts.utils.unicode.pretty_print_char(character)} on "
                        f"charline {y_index} index {x_index}.",
                    )
