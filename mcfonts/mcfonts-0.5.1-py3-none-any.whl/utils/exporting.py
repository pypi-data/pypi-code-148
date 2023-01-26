#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Functions for exporting various character/provider formats into XML-representable data.

Contains functions for handling various providers and exporting them into font XMLs.
These providers are handled:

* space
* bitmap
* legacy_unicode
* mcfonts:options
"""
import datetime

import fontTools.pens.t2CharStringPen
import lxml.etree
import PIL.Image
import mcfonts.constants
import mcfonts.exceptions
import mcfonts.utils.unicode


def glyph_to_program(
    glyph: PIL.Image.Image, ascent: int, pixel_size: float, options: dict | None = None
) -> list[str | int] | None:
    """
    Create a Type 2 charstring program given a glyph sheet.
    If the glyph is empty or has no white pixels,
    None will be returned. Otherwise, a list of strings will be.

    These charstrings are **not** optimized or checked for overlaps.
    In FontForge, use :menuselection:`E&lement --> O&verlap --> &Remove Overlap` manually
    afterwards.

    :param glyph: A :class:`PIL.Image.Image` of the individual character, **not** the font sheet.
    :param ascent: The ascent of this glyph, equal to ``(ascent - height) * (glyph_height / height)``.
    :param pixel_size: How big each pixel should be.
    :param options:
        A specialized dictionary that should be derived
        from an instance of :class:`mcfonts.providers.OptionsProvider`.
        Should be in the form of {field*: value}. For example, an Options dictionary of
        ``{"width": {"a": 4}, "spacing": {"a": 2}}``
        should transform into ``{"width": 4, "spacing": 2}``.
        Use :meth:`mcfonts.providers.OptionsProvider.get_options_for_char` for this.
    :returns:
        A list of strings of the glyph's program,
        or None if there was no pixel data in ``glyph``.
    """
    # Excess is a number of how far away the glyph is from the left edge of the canvas
    if options is None:
        options = {}
    excess = get_glyph_nominals(glyph)
    # If excess is -1 (special case), there is nothing here but a space.
    if excess[1] == -1:
        return None
    # No components to resolve, so no glyphSet is needed; using {}
    pen = fontTools.pens.t2CharStringPen.T2CharStringPen(0, {}, 0)
    modifiers = [0, 0]
    width = excess[1] + 1
    if options.get("fullwidth", False) is True:
        width = glyph.width
    # If shift is [0, 0], ignore it.
    if options.get("shift", [0, 0]) != [0, 0]:
        modifiers = options["shift"]
    if options.get("spacing") is not None:
        width = excess[1] + options["spacing"]
    if options.get("width") is not None:
        width = options["width"]
    if glyph.mode == "RGBA":
        data = glyph.getdata(3)
    elif glyph.mode == "LA":
        data = glyph.getdata(1)
    else:
        data = glyph.getdata(0)
    for index, pixel in enumerate(data):
        if pixel >= 180:
            x_position = index % glyph.width
            y_position = index // glyph.width
            pen.moveTo(
                (
                    (x_position + modifiers[0]) * pixel_size,
                    (glyph.height - y_position + ascent + modifiers[1]) * pixel_size,
                )
            )
            # Left X, top right
            pen.lineTo(
                (
                    (x_position + 1 + modifiers[0]) * pixel_size,
                    (glyph.height - y_position + ascent + modifiers[1]) * pixel_size,
                )
            )
            # Down Y, bottom left
            pen.lineTo(
                (
                    (x_position + 1 + modifiers[0]) * pixel_size,
                    (glyph.height - y_position - 1 + ascent + modifiers[1]) * pixel_size,
                )
            )
            # Right X, bottom right
            pen.lineTo(
                (
                    (x_position + modifiers[0]) * pixel_size,
                    (glyph.height - y_position - 1 + ascent + modifiers[1]) * pixel_size,
                )
            )
            # Done pixel
            pen.closePath()
    # Return the pen's resulting program
    charstring = pen.getCharString()
    # Set the width correctly
    charstring.program[0] = int(pixel_size * width)

    mcfonts.logger.debug(f"exporting: made program for glyph, with options: {bool(options)}")

    return charstring.program


def get_glyph_nominals(glyph: PIL.Image.Image) -> tuple[int, int]:
    """
    Return the number of pixels away from the left edge of the canvas the glyph is and the
    glyph's resulting calculated width.

    If return is 0, -1, there is no pixel data, the glyph is all spaces.

    :param glyph: A :class:`PIL.Image.Image` instance.
    :returns:
        Left padding and total width.
        Returns (0, -1) if no pixel data.
    """
    try:
        bbox = glyph.getbbox()
        return bbox[0], bbox[2]
    except (TypeError, IndexError):
        # Pure space, has no width
        return 0, -1


def allocate_char(font_xml: lxml.etree._Element, char: str) -> None:
    """
    Allocate a Unicode character in a font.
    Does not assign any character data or widths.

    :param font_xml: The font XML.
    :param char: A single character.
    :returns: Nothing, font is modified in-place.
    :raises GlyphLimitError: If there are more than 65,535 glyphs in the font; can't add more.
    """
    codepoint = ord(char)
    uni = f"u{codepoint:04X}"

    if (metrics_num := int((metrics := font_xml.find("hhea/numberOfHMetrics")).get("value"))) >= 65535:
        raise mcfonts.exceptions.GlyphLimitError
    metrics.set("value", str(metrics_num + 1))

    num_glyphs = font_xml.find("maxp/numGlyphs")
    num_glyphs.set("value", str(int(num_glyphs.get("value")) + 1))

    cmap = font_xml.find("cmap")

    if (cmap_12 := cmap.find("cmap_format_12")) is None:
        lxml.etree.SubElement(
            cmap,
            "cmap_format_12",
            {
                "platformID": "0",
                "platEncID": "4",
                "language": "0",
                "length": "4120",
                "nGroups": "323",
                "format": "12",
                "reserved": "0",
            },
        )
        cmap_12 = cmap.find("cmap_format_12")
    # Inside the BMP
    if codepoint <= 0xFFFF:
        # No format table exists yet, add it
        if (cmap_4 := cmap.find("cmap_format_4")) is None:
            lxml.etree.SubElement(
                cmap,
                "cmap_format_4",
                {
                    "platformID": "3",
                    "platEncID": "4",
                    "language": "0",
                },
            )
            cmap_4 = cmap.find("cmap_format_4")
        lxml.etree.SubElement(cmap_4, "map", {"code": f"0x{codepoint:X}", "name": uni, "language": "0"})
    lxml.etree.SubElement(cmap_12, "map", {"code": f"0x{codepoint:X}", "name": uni, "language": "0"})

    lxml.etree.SubElement(font_xml.find("GDEF/GlyphClassDef"), "ClassDef", {"glyph": uni, "class": "1"})

    lxml.etree.SubElement(font_xml.find("GlyphOrder"), "GlyphID", {"name": uni})
    mcfonts.logger.debug(f"exporting: allocated char {mcfonts.utils.unicode.pretty_print_char(char)}")


def set_program_to_char(font_xml: lxml.etree._Element, program: list[str], char: str, replace: bool = True) -> None:
    """
    Set a program to a character.
    This is how character data is added to the font.
    The character must be allocated already.
    That is not done in this function.

    If the character is not in the font, add it.
    If it is and ``replace`` is True, set it to the new character data.
    Otherwise, do nothing.

    :param font_xml: The font XML.
    :param program: A list of strings of the glyph's program.
    :param char: A single character.
    :param replace: If the character already has data, overwrite.
    :returns: Nothing, font is modified in-place.
    :raises GlyphLimitError: If there are more than 65,535 glyphs in the font; can't add more.
    """
    uni = f"u{ord(char):04X}"
    charstrings = font_xml.find("CFF/CFFFont/CharStrings")
    charstring_xml = font_xml.find(f"{charstrings}/CharString[@name='{uni}']")
    if charstring_xml is None:
        # Doesn't exist
        lxml.etree.SubElement(charstrings, "CharString", {"name": uni}).text = " ".join(str(x) for x in program)
        lxml.etree.SubElement(font_xml.find("hmtx"), "mtx", {"name": uni, "width": str(program[0]), "lsb": "0"})
    elif replace:
        # Exists already in the charstrings, replace it too
        charstring_xml.text = " ".join(str(x) for x in program)
        font_xml.find(f"hmtx/mtx[@name='{uni}']").set("width", str(program[0]))
    mcfonts.logger.debug(
        f"exporting: set program to char {mcfonts.utils.unicode.pretty_print_char(char)}, replaced: {replace}"
    )


def set_space_to_char(font_xml: lxml.etree._Element, char: str, width: int, replace: bool = True) -> None:
    """
    Add/set a whitespace character to the font, only defining its width.
    The charcter must be allocated already. That is not done in this function.

    If the glyph is not in the font, add it.
    If it is and ``replace`` is True, set it to the new value.
    Otherwise, do nothing.

    :param font_xml: The font XML.
    :param char: A single character.
    :param width: The width of the whitespace, unscaled.
    :param replace: If the character already has data, overwrite.
    :returns: Nothing, font is modified in-place.
    :raises GlyphLimitError: If there are more than 65,535 glyphs in the font; can't add more.
    """
    uni = f"u{ord(char):04X}"
    charstrings = font_xml.find("CFF/CFFFont/CharStrings")
    width *= 125

    if (charstring_xml := font_xml.find(f"{charstrings}/CharString[@name='{uni}']")) is None:
        # Doesn't exist
        lxml.etree.SubElement(charstrings, "CharString", {"name": uni}).text = f"{width} endchar"
        lxml.etree.SubElement(font_xml.find("hmtx"), "mtx", {"name": uni, "width": str(width), "lsb": "0"})
    elif replace:
        # Exists already in the charstrings, replace it too
        charstring_xml.text = f"{width} endchar"
        font_xml.find(f"hmtx/mtx[@name='{uni}']").set("width", str(width))
    mcfonts.logger.debug(
        f"exporting: set space to char {mcfonts.utils.unicode.pretty_print_char(char)}, "
        f"replaced: {replace}, width: {width}"
    )


def add_namerecord_to_font(font_xml: lxml.etree._Element, data: str, name_id: int) -> None:
    """
    Set a namerecord in a font.
    Does not check if such a namerecord already exists, and will add new namerecords.

    * 0 -> Copyright
    * 1 -> Font family
    * 2 -> Font subfamily
    * 3 -> Unique font ID
    * 4 -> Full font name, ID 1 + 2
    * 5 -> Version: "Version maj.min"
    * 6 -> PostScript name
    * 7 -> Trademark
    * 8 -> Manufacturer
    * 9 -> Designer
    * 10 -> Descriptions

    See more at https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids.

    All are encoded at (0, 4) and (3, 1), Unicode 2.0+ full.

    :param font_xml: The font XML.
    :param data: Whatever string to add.
    :param name_id: The ID of the namerecord.
    :returns: Nothing, font is modified in-place.
    """
    lxml.etree.SubElement(
        font_xml.find("name"),
        "namerecord",
        {"platformID": "0", "platEncID": "4", "nameID": str(name_id), "langID": "0x0"},
    ).text = data
    lxml.etree.SubElement(
        font_xml.find("name"),
        "namerecord",
        {"platformID": "3", "platEncID": "1", "nameID": str(name_id), "langID": "0x409"},
    ).text = data
    mcfonts.logger.debug(f"exporting: added namerecord {name_id}: {data}")


def set_cfffont_name(font_xml: lxml.etree._Element, font_name: str, family_name: str) -> None:
    """
    Sets the font's appropriate CFF name in 'CFF ' tables.
    This is not the same as changing the 'name' tables, see :func:`add_namerecord_to_font` instead.

    :param font_xml: The font XML.
    :param font_name: The name of the font (do not include "Regular" or related weights).
    :param family_name: The family name of the font (do not include "Regular" or related weights).
    :returns: Nothing, font is modified in-place.
    """
    cfffont = font_xml.find("CFF/CFFFont")
    cfffont.set("name", mcfonts.utils.sanitize_font_name(font_name))
    cfffont.find("FullName").set("value", font_name)
    cfffont.find("FamilyName").set("value", family_name)
    mcfonts.logger.debug(f"exporting: set CFF font name to {font_name}, family {family_name}")


def set_font_times(font_xml: lxml.etree._Element) -> None:
    """
    Sets the font's created and modified times,
    in the format of ``%a %b %d %X %Y``.

    :param font_xml: The font XML.
    :returns: Nothing, font is modified in-place.
    """
    time = datetime.datetime.now().strftime("%a %b %d %X %Y")
    font_xml.find("head/created").set("value", time)
    font_xml.find("head/modified").set("value", time)
    mcfonts.logger.debug("exporting: set font times")


def set_notdef_in_font(font_xml: lxml.etree._Element, program: list[str]) -> None:
    """
    Set the .notdef character of the font.
    The font already has a default notdef, use for setting to something else.

    :param font_xml: The font XML.
    :param program: A list of strings of the glyph's program.
    :returns: Nothing, font is modified in-place.
    """
    font_xml.find("CFF/CFFFont/CharStrings/CharString[@name='.notdef']").text = " ".join(str(x) for x in program)
    font_xml.find("hmtx/mtx[@name='.notdef']").set("width", str(program[0]))
    mcfonts.logger.debug("exporting: set notdef")


def set_font_name(font_xml: lxml.etree._Element, font_name: str, include_credits: bool = True) -> None:
    """
    Set the font's name to `font_xml` in all appropriate places.

    This not the same as :func:`set_cfffont_name`, which sets the name for only CFF tables.

    :param font_xml: The font XML.
    :param font_name: The name of the font.
    :param include_credits: If credits and links to mcfonts are included in the namerecords.
    """
    mcfonts.utils.exporting.add_namerecord_to_font(font_xml, font_name, 1)
    mcfonts.utils.exporting.set_cfffont_name(font_xml, font_name, font_name)
    mcfonts.utils.exporting.add_namerecord_to_font(font_xml, "Regular", 2)
    if include_credits:
        mcfonts.utils.exporting.add_namerecord_to_font(font_xml, "🄯 Public domain", 0)
        mcfonts.utils.exporting.add_namerecord_to_font(font_xml, f"mcfonts: {font_name} Regular: {hash(font_xml)}", 3)
        mcfonts.utils.exporting.add_namerecord_to_font(font_xml, "mcfonts", 8)
        mcfonts.utils.exporting.add_namerecord_to_font(font_xml, f"{font_name} has no trademark.", 7)
        mcfonts.utils.exporting.add_namerecord_to_font(font_xml, "https://gitlab.com/whoatemybutter/mcfonts", 11)
        mcfonts.utils.exporting.add_namerecord_to_font(
            font_xml,
            "This font is under no explicit licensing. "
            "This font's author may have additional licensing terms, contact them.",
            13,
        )
    else:
        mcfonts.utils.exporting.add_namerecord_to_font(font_xml, f"{font_name} Regular: {hash(font_xml)}", 3)
    mcfonts.utils.exporting.add_namerecord_to_font(font_xml, f"{font_name} Regular", 4)
    mcfonts.utils.exporting.add_namerecord_to_font(
        font_xml,
        f"Version 1.0; {datetime.date.strftime(datetime.date.today(), '%B %d, %Y')}",
        5,
    )
    mcfonts.utils.exporting.add_namerecord_to_font(font_xml, mcfonts.utils.sanitize_font_name(font_name), 6)
    mcfonts.utils.exporting.set_font_times(font_xml)
    mcfonts.logger.debug(f"exporting: set font name to {font_name}, credits: {include_credits}")
