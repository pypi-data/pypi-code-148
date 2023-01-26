#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
**mcfonts** is a versatile, fast, and extensible package for working with Minecraft fonts.

mcfonts works with any valid font JSON and can export every kind of texture and sizing,
no matter the format.

| For more information, see `<https://gitlab.com/whoatemybutter/mcfonts/>`_.
| Read the documentation online at `<https://mcfonts.rtfd.io>`_.

----

| Licensed under MIT license, see https://choosealicense.com/licenses/mit/ for details.
| Formatted with Black, see https://github.com/psf/black.
"""
import io
import json
import logging
import sys
import typing
import warnings

import fontTools.ttLib.ttFont
import lxml.etree
import PIL.Image
import tinyunicodeblock

import mcfonts.colors
import mcfonts.compacting
import mcfonts.constants
import mcfonts.coverage_reports
import mcfonts.exceptions
import mcfonts.providers
import mcfonts.utils.rangestring
import mcfonts.utils
import mcfonts.utils.bitmap
import mcfonts.utils.exporting

__author__ = "WhoAteMyButter"
__version__ = (0, 5)
__license__ = "MIT"


if sys.version_info < (3, 10, 0):
    raise RuntimeError(f"minimum Python version is 3.10.0, you are running {sys.version.split(' ', 1)[0]}")

# Decompression bombs will error, as they should
warnings.simplefilter("error", PIL.Image.DecompressionBombWarning)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(relativeCreated)d] [%(name)s/%(levelname)s]: (at %(funcName)s()) %(message)s",
)


class MinecraftFont:
    """
    The MinecraftFont class.
    Requires the providers of a provider file, and the associated resources mapping.

    You should never instantiate this class directly.
    Use :mod:`mcfonts.importing`.

    If you need to add, modify, or remove providers,  do it through :attr:`self.providers`.
    It's a list of Provider classes, each containing relevant fields and methods.

    Be sure to run :meth:`mcfonts.MinecraftFont.validate` after making any changes;
    it will not be done automatically.

    .. warning::
        | If more than one :class:`mcfonts.providers.OptionsProvider` is present in
        | `provider_list`, only the **last** one will be used.

    :param provider_list:
        A list of providers, all of which are instances of :data:`mcfonts.AnyProvider`.
    :param is_monochrome:
        Whether font resources are loaded with RGBA or not.
        Default is True.
    """

    def __init__(
        self,
        provider_list: list[mcfonts.providers.AnyProvider],
        is_monochrome: bool = True,
    ):
        self.providers: list[mcfonts.providers.AnyVanillaProvider] = []
        self.options: mcfonts.providers.OptionsProvider | None = None
        for provider in provider_list:
            if isinstance(provider, mcfonts.providers.OptionsProvider):
                self.options = provider
            else:
                self.providers.append(provider)
        self.glyph_cache: dict[str, dict[str, PIL.Image.Image] | dict[str, int]] = {
            "bitmap": {},
            "space": {},
        }
        for provider in self.providers:
            if isinstance(provider, mcfonts.providers.BitmapProvider):
                self.glyph_cache["bitmap"].update(provider.glyphs)
            elif isinstance(provider, mcfonts.providers.SpaceProvider):
                self.glyph_cache["space"].update(provider.contents["advances"])
        self.is_monochrome: bool = is_monochrome

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.providers + [self.options]}, {self.is_monochrome})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __hash__(self) -> int:
        return hash((self.providers, self.glyph_cache, self.is_monochrome, self.options))

    def __add__(self, other: "MinecraftFont"):
        # Make a copy of it
        first = MinecraftFont(self.providers, self.is_monochrome)
        # iadd
        first += other
        return first

    def __iadd__(self, other: "MinecraftFont"):
        self.providers += other.providers
        self.glyph_cache |= other.glyph_cache
        if other.is_monochrome is False:
            self.is_monochrome = False
        self.validate()
        return self

    def __len__(self):
        return self.count_coverage()

    def export(
        self,
        font_name: str,
        character_filter: mcfonts.providers.CharacterFilter | None = None,
        provider_filter: mcfonts.providers.ProviderFilter | None = None,
        include_credits: bool = True,
    ) -> fontTools.ttLib.TTFont:
        """
        Export the Minecraft font into an OpenType font with Type 2 Charstring outlines.

        The font is crafted through a TTX file (font XML), and characters are added in tables and
        given simple name mappings: ``("u0954", "u1fae4", "u2605")``.

        For some fields, the font's name will be "Minecraft <font name>".

        Font must not contain over 65,535 characters, or else any additional characters
        will not be added, and the font will be saved prematurely.

        :param font_name:
            The name of the resulting font, not what its filename is.
            This will be passed to :func:`mcfonts.utils.sanitize_font_name`.
        :param character_filter: An optional instance of :class:`mcfonts.exporting.CharacterFilter`.
        :param provider_filter: An optional instance of :class:`mcfonts.exporting.ProviderFilter`.
        :param include_credits:
            To include basic copyright information and credits in the font file.
        """
        font_xml = mcfonts.constants.XML_FONT_TEMPLATE
        allocated_chars: set[str] = set()
        num_providers = 0
        # Set the space character pre-emptively
        mcfonts.utils.exporting.set_space_to_char(font_xml, " ", 4)
        for provider in self.providers:
            if not provider or (provider_filter and provider_filter.should_ignore_provider(provider.__class__)):
                logger.info(f"Skipping provider {mcfonts.providers.pretty_print_provider(provider)}")
                continue
            logger.info(f"Working on provider {mcfonts.providers.pretty_print_provider(provider)}")
            try:
                if isinstance(
                    provider,
                    (
                        mcfonts.providers.BitmapProvider,
                        mcfonts.providers.LegacyUnicodeProvider,
                    ),
                ):
                    allocated_chars.update(provider.export(font_xml, allocated_chars, self.options, character_filter))
                elif isinstance(provider, mcfonts.providers.SpaceProvider):
                    # Space has no options
                    allocated_chars.update(provider.export(font_xml, allocated_chars, character_filter))
                elif isinstance(provider, mcfonts.providers.TTFProvider):
                    print("Cannot do work for TTF files, skipping.")
                else:
                    logger.warning(mcfonts.providers.format_provider_message(provider, "is an unknown type, skipping."))
                    continue
                num_providers += 1
            except mcfonts.exceptions.GlyphLimitError:
                logger.warning("Font has too many characters (over 65,535), truncating and saving immediately.")
                break
        mcfonts.utils.exporting.set_font_name(font_xml, font_name, include_credits)
        logger.info("Compiling...")
        font = fontTools.ttLib.ttFont.TTFont(recalcTimestamp=False, recalcBBoxes=False, sfntVersion="OTTO")
        font.importXML(io.StringIO(lxml.etree.tostring(font_xml, encoding=str)))
        logger.info(f"Exported {len(allocated_chars):,} characters from {num_providers:,} provider(s).")
        return font

    def count_coverage(self) -> int:
        """
        Count the number of glyphs this font covers (has a definition for).

        Characters that are encoded in more than 1 UTF-16 codepoint are counted correctly (SMP+).
        Skin tones, presentation modifiers, combining symbols, etc. are separate characters.

        Characters like U+2414F 𤅏 and U+2603 ☃ have the same length.

        :returns: Number of characters supported.
        """
        return len(self.glyph_cache["bitmap"] | self.glyph_cache["space"])

    def get_chars_covered(self) -> typing.Iterator[str]:
        """
        Yield all the characters this font covers (has a definition for).

        Spaces and null bytes are not counted for the "bitmap" provider.
        "Space" providers are counted.
        """
        for character in self.glyph_cache["bitmap"] | self.glyph_cache["space"]:
            yield character

    def write(self, output_file: str, indent: int | str | None = 4) -> None:
        """
        Simply write the font JSON to a file.
        This is not the same as exporting.

        The file is indented by default.
        If a file exists at ``file_location``, it will be overwritten.

        .. warning:: Not to be confused with :func:`export()`.

        :param output_file:
            File path to write to.
        :param indent:
            The indentation level, refer to :func:`json.dump()` for possible values.
        """
        with open(mcfonts.utils.expand_path(output_file), "w", encoding="utf-8") as open_file_location:
            write_providers = [x.contents for x in self.providers]
            if self.options:
                write_providers += self.options.contents
            json.dump({"providers": write_providers}, open_file_location, ensure_ascii=False, indent=indent)

    def count_providers(self) -> dict[str, int]:
        """
        Return a counted summary of the providers this font contains.

        This is future-proof, and will work with any provider as long as it has a "type" key.

        :returns: A summary of font's providers.
        """
        result = {}
        for provider in self.providers:
            if (provider_type := provider.provider_type) not in result:
                result[provider_type] = 1
            else:
                result[provider_type] += 1
        return result

    def count_providers_total(self) -> int:
        """
        Count the number of providers in the font.

        :returns: Number of providers.
        """
        return len(self.count_providers())

    def print_info(self, table_chars: bool = True, summary_only: bool = False) -> None:
        """
        Print basic information about the font.

        :param table_chars:
            Whether to print a 'chars' list as a square table, or as a simple string.
            This only applies to :class:`mcfonts.providers.BitmapProvider`.
        :param summary_only:
            If True, will only print the number of characters and providers.
        """
        if not summary_only:
            for provider in self.providers:
                if isinstance(provider, mcfonts.providers.BitmapProvider):
                    provider.print_info(table_chars)
                else:
                    provider.print_info()
            print("\n")
        print(f"Characters: {self.count_coverage():,}")
        print(f"Providers: {self.count_providers_total():,}")

    def validate(self) -> None:
        """
        Run basic structure checks on the providers of the font JSON.
        """
        if len(self.providers) < 1:
            logger.warning("There are no providers.")
        for provider in self.providers:
            if isinstance(provider, mcfonts.providers.Provider):
                provider.validate()
            else:
                raise mcfonts.exceptions.ProviderError(
                    mcfonts.providers.format_provider_message(provider, "is not a valid provider.")
                )

    def compact(
        self,
        chars_in_row: int = 0,
        cell_size: tuple[int, int] = (0, 0),
        square_cells: bool = True,
        output_file: str | None = None,
    ) -> tuple[list[str], PIL.Image.Image, tuple[int, int]]:
        """
        Take all "bitmap" providers and export every character sheet into a single sheet.
        Characters are scaled according to the largest effective bounding box in all providers.

        This uses :func:`mcfonts.utils.bitmap.compact_providers_single` behind the scenes.

        :param chars_in_row:
            How many characters to fit inside each row of the resulting sheet.
            If this is 0, this will be set to the length of the first string in the
            "charlist" list. If this is negative, this will be set so that the resulting sheet is
            square. By default, this is 0 (auto first string).
        :param cell_size:
            What size to make each glyph cell.
            If this is (0, 0),
            this will be set to the largest dimensions of every glyph in `glyphs`.
            If this is any other tuple of numbers, TODO actually finish this
        :param square_cells:
            If True, each glyph's width will equal its height.
            This is based on whichever number is largest.
            If False, each glyph's width will be unrelated to its height.
        :param output_file: Where to write the sheet to. If this is None, nothing will be
            written.
        :returns: A list of the new characters, and the new file as a :class:`PIL.Image.Image`.
        """
        sheet = mcfonts.compacting.compact_providers(self.providers, chars_in_row, cell_size, square_cells)
        if output_file:
            with open(mcfonts.utils.expand_path(output_file), "wb") as open_output_file:
                sheet[1].save(open_output_file)
        return sheet

    def coverage_report(self) -> mcfonts.coverage_reports.CoverageReport:
        """
        Build a report of what characters this font contains.

        This includes information like how many characters are in the font,
        and what Unicode blocks are covered.

        :returns: A dictionary of ``{"chars": int, "blocks": {str: int}}``.
        """
        chars: list[str] = []
        blocks: dict[str, int] = {}
        for char in self.get_chars_covered():
            chars.append(char)
            if (block := tinyunicodeblock.block(char, include_csur=True)) in blocks:
                blocks[block] += 1
            else:
                blocks[block] = 1
        return mcfonts.coverage_reports.CoverageReport(set(chars), blocks)

    def get_glyphs_in_rangestring(self, rangestring: str) -> dict[str, PIL.Image.Image | None]:
        """
        Given a `rangestring`,
        return a dictionary of the requested chars to their glyphs.

        :param rangestring:
            A string representing the requested range of chars.
            See :func:`mcfonts.utils.rangestring_to_range` for details.
        :returns: A list of the requested glyphs that match `rangestring`.
        """
        glyphs: dict[str, PIL.Image.Image | None] = {}
        for provider in self.providers:
            if isinstance(provider, mcfonts.providers.BitmapProvider):
                glyphs |= dict(provider.get_glyphs_in_rangestring(rangestring))
        return glyphs

    def get_covering_providers(self, rangestring: str) -> list[mcfonts.providers.AnyVanillaProvider]:
        """
        Given a codepoint range,
        return a list of :class:`mcfonts.providers.AnyProvider` that cover these chars.

        :param rangestring:
            A string representing the requested range of chars.
            See :func:`mcfonts.utils.rangestring_to_range` for details.
            Essentially, accepts any of these:

            * 16FF => one codepoint, 5887
            * 2000-22ff => range of chars from 8192 to 8959
            * U+5460..5800 => range of chars from 21600 to 22528
            * U+6000..6001 => range of chars from 24576 to 24577
            * A-Z => range of chars from 65 to 90
            * ☃ => one codepoint, 9731

            Ranges can be split by commas.
        :returns: A list of the providers that cover codeopints defined in `rangestring`.
        """
        result = []
        covers = mcfonts.utils.rangestring.rangestring_to_characters(rangestring)
        for provider in self.providers:
            if not isinstance(provider, mcfonts.providers.SpaceProvider):
                # Ignore padding chars
                covers.difference_update(mcfonts.constants.PADDING_CHARS)
            if provider.chars_covered.intersection(covers):
                result.append(provider)
        return result

    def reload_to_monochrome(self):
        """
        Replace the resources used in the providers with a grayscale version.
        If the resource is already grayscale, this will have no effect.

        This modifies the resource of this provider in place, and **cannot be undone**.
        """
        if self.is_monochrome:
            mcfonts.logger.info("Font is already in monochrome; can't reload")
            return
        for provider in self.providers:
            if isinstance(provider, mcfonts.providers.BitmapProvider):
                provider.reload_to_monochrome()
        self.is_monochrome = True

    def compare(self, other: "MinecraftFont"):
        """
        Given `other`, a second instance of :class:`~mcfonts.MinecraftFont`,
        compare the two, using `self` as a baseline.

        The information compared is:

        * Character count
        * Blocks covered
        * Providers included

        :param other: A second instance of :class:`mcfonts.MinecraftFont` to compare to.
        :returns: Nothing, this function prints its results.
        """
        self.coverage_report().compare(other.coverage_report())
        if mcfonts.colors.USE_COLORS:
            print(f"\n{mcfonts.colors.BRIGHT}PROVIDERS{mcfonts.colors.RESET_ALL}")
        else:
            print("\nPROVIDERS")
        print(":: type: this | other (delta)")
        providers_this = {"bitmap": 0, "space": 0, "ttf": 0, "legacy_unicode": 0}
        providers_other = providers_this.copy()
        for provider in self.providers:
            providers_this[provider.provider_type] += 1
        for provider in other.providers:
            providers_other[provider.provider_type] += 1
        for provider_type in ("bitmap", "space", "ttf", "legacy_unicode"):
            amount_this = providers_this[provider_type]
            amount_other = providers_other[provider_type]
            print(
                f"\t{provider_type}: "
                f"{amount_this} | {amount_other} "
                f"({mcfonts.utils.color_number(amount_other-amount_this)})"
            )
