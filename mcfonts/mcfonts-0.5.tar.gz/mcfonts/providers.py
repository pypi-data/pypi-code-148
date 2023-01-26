#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Contains the Provider classes and the CharacterFilter and ProviderFilter."""
import math
import typing
import unicodedata

import jsonschema
import lxml.etree
import PIL.Image

import mcfonts
import mcfonts.constants
import mcfonts.exceptions
import mcfonts.utils.exporting
import mcfonts.utils.unicode
import mcfonts.utils
import mcfonts.utils.bitmap
import mcfonts.utils.rangestring


class Provider:
    """The base provider class."""

    def __init__(self, provider_type: str, contents: dict, chars_covered: set[str] | None = None):
        if chars_covered is None:
            chars_covered = set()
        self.provider_type: str = provider_type
        self.chars_covered: set[str] = chars_covered
        self.contents: dict = contents

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f'"{self.provider_type}", {self.chars_covered}, {self.contents})'

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({len(self.chars_covered)} chars)"

    def validate(self) -> None:
        """
        Specific tests for validating a provider.

        Values are checked to ensure that they're correct and in an acceptable range.
        Textures are checked to ensure all characters have a defined glyph,
        and that the dimensions are correct.

        Warnings are printed through :func:`logger.warning`.

        :returns: Nothing; problems are either raised or warned.
        """

    def print_info(self) -> None:
        """Print information about this provider."""
        print(f"Provider type: {self.provider_type or mcfonts.constants.UNKNOWN_FIELD}")
        print(f"Characters covered: {len(self.chars_covered)}")


class OptionsProvider(Provider):
    """A mcfonts-specific provider that only is used when exporting."""

    def __init__(self, provider: dict):
        self.contents = provider.copy()
        self.contents["fields"] = {}

        # Expand the rangestrings, copy over fields
        for field in mcfonts.constants.OPTION_FIELDS:
            if field not in self.contents["fields"]:
                self.contents["fields"][field] = {}
            for key, value in provider.get("fields", {}).get(field, {}).items():
                for newchar in mcfonts.utils.rangestring.rangestring_to_characters(key):
                    self.contents["fields"][field][newchar] = value
        chars_covered: set[str] = set()
        for field in mcfonts.constants.OPTION_FIELDS:
            chars_covered.update(self.contents["fields"].get(field, {}).keys())
        # Explicitly put mcfonts:options
        super().__init__("mcfonts:options", self.contents, chars_covered)
        self.validate()

    def validate(self) -> None:
        """
        Validate a bitmap provider,
        ensuring its structure is correct and that all values are acceptable.

        This function does validate textures.

        :returns: Nothing; problems are either raised or warned.
        """
        jsonschema.validate(self.contents, mcfonts.constants.SCHEMA_PROVIDER_OPTIONS)
        for char in self.chars_covered:
            if self.contents.get("fullwidth", {}).get(char) and self.contents.get("spacing", {}).get(char):
                mcfonts.logger.warning(
                    format_provider_message(
                        self, f"has conflicting options, fullwidth and spacing are present for character {char}."
                    )
                )
            if self.contents.get("fullwidth", {}).get(char) and self.contents.get("width", {}).get(char):
                mcfonts.logger.warning(
                    format_provider_message(
                        self, f"has conflicting options, fullwidth and width are present for character {char}."
                    )
                )
            if self.contents.get("width", {}).get(char) and self.contents.get("spacing", {}).get(char):
                mcfonts.logger.warning(
                    format_provider_message(
                        self, f"has conflicting options, width and spacing are present for character {char}."
                    )
                )

    def get_options_for_char(self, char: str) -> dict[str, int | bool] | None:
        """
        Given `char`, a character, return a dictionary of all the options for that character.

        For example, if :attr:`self.contents` is:
            {"width": {"a": 4}, "spacing": {"a": 0}}
        Then `self.get_options_for_char("a")` should return:
            {"width": 4, "spacing": 0}

        :param char: A single character.
        :returns: A flat dictionary containing a value for each field that `char` has declared.
        """
        result = {}
        for field in mcfonts.constants.OPTION_FIELDS:
            if (char_options := self.contents["fields"].get(field, {}).get(char)) is not None:
                result[field] = char_options
        if result:
            return result
        return None

    def has_options(self, char: str, field_names: str | set[str] | None = None) -> bool:
        """
        Given `char`, a character, return if any options are defined for it.
        If `field_names` is not None, only return True if the character has an option for that field.

        :param char:
            A single character.
        :param field_names:
            Either a string, list of strings, or None.
            If str, check for this field name only.
            If list[str], check for *any* of these field names.
            If None, no special field check.
        :returns: If `char` has an option declared for it.
        """
        if isinstance(field_names, str):
            fields = {field_names}
        elif isinstance(field_names, set):
            fields = field_names
        else:
            fields = mcfonts.constants.OPTION_FIELDS
        for field in fields:
            if (self.contents["fields"].get(field, {}).get(char)) is not None:
                return True
        return False


class CharacterFilter:
    """
    A character filter, for use in :meth:`mcfonts.providers.AnyVanillaProvider.export`.
    These are passed into these functions, and control what characters are added, and on what conditions.
    """

    def __init__(
        self,
        select_chars: set[str] | str | None = None,
        chars_policy: typing.Literal["include", "exclude"] = "include",
        options: OptionsProvider | None = None,
        options_policy: typing.Literal["include", "ignore", "include_only", "ignore_only"] = "include",
    ):
        """
        :param select_chars:
            A set of characters that will be either included or excluded from the exported font.

            If this is a string, it must be a :doc:`rangestring <rangestrings>`.

            For how to control this selection's effect, see `chars_policy`.
            If this is an empty set, it will be ignored, regardless of what `chars_policy` is.
        :param chars_policy:
            How to handle `select_chars`:

            * "include": Only characters that are in this set will be exported *(default)*.
            * "exclude": Characters that are in this set will not be exported.
        :param options:
            An optional :class:`OptionsProvider` instance.
            If supplied, exported characters will obey it.
        :param options_policy:
            How to handle `options`:

            * If "include", include characters that have options declared.
            * If "ignore", disregard the options for a char, even if declared (but still include the char)
            * If "include_only", only include characters that have options declared.
            * If "ignore_only", only include characters that don't have any options declared.
        """
        if isinstance(select_chars, str):
            select_chars = mcfonts.utils.rangestring.rangestring_to_characters(select_chars)
        self.select_chars: set[str] | None = select_chars
        self.chars_policy: typing.Literal["include", "exclude"] = chars_policy
        self.options: mcfonts.providers.OptionsProvider | None = options
        self.options_policy: typing.Literal["include", "ignore", "include_only", "ignore_only"] = options_policy

    def should_ignore_char(self, character: str) -> int:
        """
        Determine how to handle `character`.
        Returns an integer describing how to proceed.

        :param character: A single character.
        :returns:
            An integer describing how to proceed:

            0: Proceed as normal
            1: Ignore this char
            -1: Ignore the options for this char, but include the char
        """
        if self.select_chars and (
            (self.chars_policy == "ignore" and character in self.select_chars)
            or (self.chars_policy == "include" and character not in self.select_chars)
        ):
            return 1

        if self.options is not None:
            if self.options.has_options(character):
                if self.options_policy in ("include_only", "include"):
                    return 0
                if self.options_policy == "ignore":
                    return -1
                if self.options_policy == "ignore_only":
                    return 1
            if self.options_policy == "include_only":
                return 1
        return 0


class BitmapProvider(Provider):
    """
    A bitmap provider.
    """

    def __init__(self, provider: dict, resource: PIL.Image.Image | None):
        self.contents = provider
        # Default height fallback
        self.contents["height"] = self.contents.get("height", 8)
        self.resource = resource
        if self.resource:
            if len(self.contents["chars"]) > 0:
                self.glyph_cell = (
                    self.resource.width // len(self.contents["chars"][0] or ""),
                    self.resource.height // len(self.contents["chars"]),
                )
            else:
                self.glyph_cell = (self.resource.width, self.resource.height)
        else:
            self.glyph_cell = (0, 0)
        self.validate()

        # Ensure resource exists before calculating glyph cell box
        self.glyphs: dict[str, PIL.Image.Image] = dict(self.yield_glyphs())

        super().__init__(
            "bitmap",
            self.contents,
            set(char for charline in self.contents["chars"] for char in charline) - mcfonts.constants.PADDING_CHARS,
        )

    def export(
        self,
        font_xml,
        already_allocated_chars: set[str],
        options: OptionsProvider | None = None,
        character_filter: CharacterFilter | None = None,
    ) -> set[str]:
        """
        Export a bitmap provider to a font XML.

        Options are honored, regardless of whatever the exporting function above says.
        To disable this, set ``options = {}`` before passing it in.

        The font XML is modified in-place.

        :param font_xml: The font XML.
        :param already_allocated_chars: A set of the allocated chars in `font_xml`.
        :param options:
            An optional :class:`OptionsProvider` instance.
            If supplied, exported characters will obey it.
        :param character_filter: An optional instance of :class:`mcfonts.providers.CharacterFilter`.
        :returns: A new set of the characters added only in this provider.
        """
        # Ensure there's work to be done (there's chars to export) before even trying
        # also ensure that there's a resource to grab glyphs from
        if (
            len(self.contents["chars"]) < 1
            or not mcfonts.utils.bitmap.assert_charlist_is_equal(self.contents["chars"])[0]
            or not self.resource
        ):
            return set()
        allocated_chars = []
        for charline in self.contents["chars"]:
            if mcfonts.utils.is_charline_empty(charline):
                continue
            for character in charline:
                char_options = options.get_options_for_char(character)
                if character in mcfonts.constants.PADDING_CHARS:
                    continue
                if character_filter:
                    should_proceed = character_filter.should_ignore_char(character)
                    if should_proceed == 1:
                        continue
                    if should_proceed == -1:
                        char_options = None
                if glyph := self.glyphs.get(character):
                    if character not in already_allocated_chars:
                        # Only allocate the character if it doesn't exist
                        mcfonts.utils.exporting.allocate_char(font_xml, character)
                        allocated_chars.append(character)
                    if program := mcfonts.utils.exporting.glyph_to_program(
                        glyph,
                        (self.contents["ascent"] - self.contents["height"])
                        * (self.glyph_cell[1] // self.contents["height"]),
                        # Em size (1000) divided by 8 (standard width) = 125,
                        # divide by scale to get how big each "pixel" will translate to
                        125 / (self.glyph_cell[1] / self.contents["height"]),
                        char_options,
                    ):
                        mcfonts.utils.exporting.set_program_to_char(font_xml, program, character)
                    else:
                        # Nothing here, it was a space.
                        mcfonts.logger.debug(
                            f"Glyph for {mcfonts.utils.unicode.pretty_print_char(character)} is "
                            f"empty, replacing with a 1-wide space."
                        )
                        mcfonts.utils.exporting.set_space_to_char(font_xml, character, 1)
        return set(allocated_chars)

    def validate(self) -> None:
        """
        Validate a bitmap provider,
        ensuring its structure is correct and that all values are acceptable.

        This function does validate textures.

        :returns: Nothing; problems are either raised or warned.
        """
        jsonschema.validate(self.contents, mcfonts.constants.SCHEMA_PROVIDER_BITMAP)
        mcfonts.utils.bitmap.validate_charlist(self.contents["chars"], self.resource, self.glyph_cell)
        if self.resource:
            height = self.contents["height"]
            glyph_height = self.glyph_cell[1]
            if glyph_height % height != 0:
                mcfonts.logger.warning(
                    format_provider_message(
                        self,
                        f"has an invalid height ({height}), "
                        f"it must be a multiple of the glyph's height ({glyph_height})",
                    )
                )
            if self.glyph_cell[0] > 256 or self.glyph_cell[1] > 256:
                # The limit for a character is 256, anything beyond that is an error in
                # atlas-stitching
                # Will still try to make it work but makes no guarantee
                mcfonts.logger.warning(
                    format_provider_message(
                        self,
                        "has excessively large glyph size, maximum character cell size is 256, "
                        f"but got {max(self.glyph_cell[0], self.glyph_cell[1])}.",
                    )
                )

    def get_glyphs_in_rangestring(self, rangestring: str) -> typing.Iterator[tuple[str, PIL.Image.Image | None]] | None:
        """
        Given `rangestring`,
        return a dictionary of the requested characters to their glyphs.

        A rangestring is a comma-separated string of characters or range notations.
        Essentially, accepts any of these:

        * 16FF => one codepoint, 5887
        * 2000-22ff => range of codepoints from 8192 to 8959
        * U+5460..5800 => range of codepoints from 21600 to 22528
        * U+6000..6001 => range of codepoints from 24576 to 24577
        * A-Z => range of codepoints from 65 to 90
        * ☃ => one codepoint, 9731

        Ranges can be split by commas.

        :param rangestring:
            A string representing the requested range of chars.
            See :func:`mcfonts.utils.ranges_from_rangestring()` for details.
        :returns:
            A yield of the requested glyphs that match `rangestring`,
            or None if there are no such matching glyphs.
        """
        if not self.resource:
            return {}
        wanted: set[str] = mcfonts.utils.rangestring.rangestring_to_characters(rangestring)
        for y_index, charline in enumerate(self.contents["chars"]):
            if mcfonts.utils.is_charline_empty(charline):
                # Line is only spaces or null padding, ignore it entirely to save time
                continue
            for x_index, char in enumerate(charline):
                # Is character not null nor space and
                # is there an actual glyph there (parameters permitting)
                if char not in mcfonts.constants.PADDING_CHARS and char in wanted:
                    glyph = self.resource.crop(
                        (
                            x_index * self.glyph_cell[0],
                            y_index * self.glyph_cell[1],
                            (x_index + 1) * self.glyph_cell[0],
                            (y_index + 1) * self.glyph_cell[1],
                        )
                    )
                    if not mcfonts.utils.is_image_empty(glyph):
                        yield char, glyph
                    else:
                        yield char, None
        return {}

    def print_info(self, table_chars: bool = True) -> None:
        """
        Print information about this provider.

        :param table_chars:
            Whether to print a 'chars' list as a square table, or as a simple string.
        """
        super().print_info()
        print(f"File: {self.contents.get('file', mcfonts.constants.UNKNOWN_FIELD)}")
        print(f"Height: {self.contents.get('height', mcfonts.constants.UNKNOWN_FIELD)}")
        print(f"Ascent: {self.contents.get('ascent')}")
        if table_chars:
            print(f"Chars: ({len(self.contents['chars'][:1]):,}x{len(self.contents['chars']):,})")
            for charline in self.contents["chars"]:
                print(f"\t{' '.join(charline)}")
        else:
            print(f"Chars: {' '.join(''.join(self.contents['chars']))}")
        print(f"Count: {sum(len(x) for x in self.contents['chars']):,}")

    def yield_glyphs(
        self,
        ignore_empty_textures: bool = False,
    ) -> typing.Iterator[tuple[str, PIL.Image.Image | None]]:
        """
        Extract every textured glyph from this provider.
        Optionally, include the height and ascent.

        :param ignore_empty_textures: Whether to not include characters that have no pixel data.
        :returns: A yield of {codepoint: glyph | None}.
        """
        if not self.resource:
            return {}
        for y_index, charline in enumerate(self.contents["chars"]):
            if mcfonts.utils.is_charline_empty(charline):
                # Line is only spaces or null padding, ignore it entirely to save time
                continue
            for x_index, char in enumerate(charline):
                # Is character not null nor space and
                # is there an actual glyph there (parameters permitting)
                if char not in mcfonts.constants.PADDING_CHARS:
                    glyph = self.resource.crop(
                        (
                            x_index * self.glyph_cell[0],
                            y_index * self.glyph_cell[1],
                            (x_index + 1) * self.glyph_cell[0],
                            (y_index + 1) * self.glyph_cell[1],
                        )
                    )
                    empty = mcfonts.utils.is_image_empty(glyph)
                    if empty or not ignore_empty_textures:
                        yield char, glyph
                    elif empty and ignore_empty_textures:
                        yield char, None
        return {}

    def get_glyph_for_char(self, char: str) -> PIL.Image.Image | None:
        """
        Extract a desired character's sheet from this provider.

        Glyph textures that are mapped to spaces or null padding return None.
        If there is more than one sheet mapped to a character (duplicate characters),
        the first occurance will be returned.

        .. warning::
            This method is not efficient. Do not use it repeatedly,
            use :func:`get_glyphs_from_providers` and get each glyph from there.

        :param char: A single character.
        :returns: A :class:`PIL.Image.Image`, or None if no glyph exists.
        """
        # Ignore non-bitmap provider or if codepoint is null or space
        # (glyphs can't be assigned for padding characters)
        if char in mcfonts.constants.PADDING_CHARS or self.resource is None:
            return None
        for y_index, charline in enumerate(self.contents["chars"]):
            if mcfonts.utils.is_charline_empty(charline):
                # Line is only spaces or null padding, ignore it entirely to save time
                continue
            for x_index, character in enumerate(charline):
                if char == character:
                    return self.resource.crop(
                        (
                            x_index * self.glyph_cell[0],
                            y_index * self.glyph_cell[1],
                            (x_index + 1) * self.glyph_cell[0],
                            (y_index + 1) * self.glyph_cell[1],
                        )
                    )
        return None

    def reload_to_monochrome(self) -> None:
        """
        Replace the resource used in this provider with a grayscale version.
        If the resource is already grayscale, this will have no effect.

        This modifies the resource of this provider in place, and **cannot be undone**.
        """
        if self.resource:
            if self.resource.mode == "LA":
                return
            self.resource = self.resource.convert("LA")


class SpaceProvider(Provider):
    """A space provider."""

    def __init__(self, provider: dict):
        self.contents = provider.copy()
        self.contents["advances"] = {}
        # Expand the rangestrings, copy over fields
        for key, value in provider.get("advances", {}).items():
            for newchar in mcfonts.utils.rangestring.rangestring_to_characters(key):
                self.contents["advances"][newchar] = value
        self.validate()
        super().__init__("space", provider, set(self.contents["advances"].keys()))

    def export(
        self,
        font_xml: lxml.etree._Element,
        already_allocated_chars: set[str],
        character_filter: CharacterFilter | None = None,
    ) -> set[str]:
        """
        Export a space provider to a font XML.
        The font XML is modified in-place.

        :param font_xml: The font XML.
        :param already_allocated_chars: A set of the allocated chars in `font_xml`.
        :param character_filter: An optional instance of :class:`mcfonts.providers.CharacterFilter`.
        :returns: A new set of the characters added only in this provider.
        """
        allocated_chars = []
        for character, width in self.contents["advances"].items():
            if character_filter and character_filter.should_ignore_char(character) == 1:
                continue
            if math.isinf(width) or math.isnan(width):
                # Some values may be infinite, limit them to 20
                width = 20
            if character not in already_allocated_chars:
                # Only allocate the character if it doesn't exist
                mcfonts.utils.exporting.allocate_char(font_xml, character)
                allocated_chars.append(character)
            mcfonts.utils.exporting.set_space_to_char(font_xml, character, abs(int(width)))
        return set(allocated_chars)

    @staticmethod
    def to_glyph_sizes(advances: dict[str, int], default_width: tuple[int, int] = (0, 14)) -> bytearray:
        """
        Create a glyph_sizes.bin bytearray from a template of chars and their starting and
        ending positions.

        :param advances: A dictionary of `{character: width}`.
        :param default_width:
            The width to fall back to if `advances` does not define one for a character.
        :returns: Bytearray of glyph_sizes.bin.
        """
        glyphsizes = bytearray((default_width[0] * 16 + default_width[1]).to_bytes(1, "big") * 65536)
        for character, width in advances.items():
            if (codepoint := ord(character)) > 0xFFFF:
                # Cannot pack characters higher than the BMP
                mcfonts.logger.warning(
                    f"Cannot include character {character} in glyph_sizes; " "codepoint is above U+FFFF."
                )
                continue
            # Ensure the high and low bits are in correct 0-F range
            if 0 > width < 15:
                raise ValueError("Width must be within 0 to 15")
            glyphsizes[codepoint] = width
        return glyphsizes

    def validate(self) -> None:
        """
        Validate a "space" provider,
        ensuring its structure is correct and that all values are acceptable.

        :returns: Nothing; problems are either raised or warned.
        """
        jsonschema.validate(self.contents, mcfonts.constants.SCHEMA_PROVIDER_SPACE)

    def print_info(self) -> None:
        """
        Print information about this provider.
        """
        super().print_info()

        if len(self.contents["advances"]) < 1:
            # There's no advances
            print("No advances.")
        else:
            advances = self.contents["advances"]
            print(f"Advances: ({len(advances)})")
            for spacechar, width in advances.items():
                print(f"\tCharacter {mcfonts.utils.unicode.pretty_print_char(spacechar)}: {width}")


class TTFProvider(Provider):
    """
    A TTF provider.
    """

    def __init__(self, provider: dict, resource: bytes | None = None):

        self.contents = provider
        if "skip" in self.contents:
            chars = []
            if isinstance(skip := self.contents.get("skip"), list):
                for line in skip:
                    chars.append(line)
            # Flatten into a string
            self.contents["skip"] = "".join(chars)
        self.validate()
        self.resource = resource
        super().__init__("ttf", provider)

    def validate(self) -> None:
        """
        Validate a "ttf" provider,
        ensuring its structure is correct and that all values are acceptable.

        .. warning:: This function does not validate textures.

        :returns: Nothing; problems are either raised or warned.
        """
        jsonschema.validate(self.contents, mcfonts.constants.SCHEMA_PROVIDER_TTF)


class LegacyUnicodeProvider(Provider):
    """A legacy unicode provider."""

    def __init__(self, provider: dict, resources: dict[str, PIL.Image.Image | bytes]):
        self.contents = provider
        self.validate()
        self.resources = {}
        # Only take resources that are relevant
        split = self.contents["template"].split("%s", 1)
        for name in resources:
            if (name.startswith(split[0]) and name.endswith(split[1])) or name == self.contents["sizes"]:
                self.resources[name] = resources[name]
        self.codepages_covered: list[int] = []
        super().__init__(
            "legacy_unicode",
            self.contents,
            # U+0000 to U+FFFF.
            set(chr(i) for i in range(65535)),
        )

    def export(
        self,
        font_xml: lxml.etree._Element,
        already_allocated_chars: set[str],
        options: OptionsProvider | None = None,
        character_filter: CharacterFilter | None = None,
    ) -> set[str]:
        """
        Export a legacy unicode provider to a font XML.
        The font XML is modified in-place.

        Despite Vanilla behavior, this function **does not** make assumptions about dimensions or
        scale.

        :param font_xml: The font XML.
        :param already_allocated_chars: A set of the allocated chars in `font_xml`.
        :param options:
            An optional :class:`OptionsProvider` instance.
            If supplied, exported characters will obey it.
        :param character_filter: An optional instance of :class:`mcfonts.providers.CharacterFilter`.
        :returns: A new set of the characters added only in this provider.
        """
        allocated_chars = []
        for unicode_codepage in range(255):
            if unicode_codepage in range(216, 223):
                # Codepage is in surrogate range, there must be nothing here
                continue
            template_parts: list[str] = self.contents["template"].split("%s")
            mcfonts.logger.info(f"Working on Unicode page {unicode_codepage:X}.")
            resource: PIL.Image.Image | None = self.resources.get(
                f"{template_parts[0]}{unicode_codepage:02x}{template_parts[1]}"
            )
            if resource is None:
                mcfonts.logger.debug(f"Provider has missing unicode page {unicode_codepage:02X}, ignoring.")
                continue
            # Calculate each character's bounding box
            resolution: tuple[int, int] = (
                resource.width // 16,
                resource.height // 16,
            )
            scale = resource.height / resolution[1]
            for y_index in range(16):
                for x_index in range(16):
                    character = chr(unicode_codepage * 256 + y_index * 16 + x_index)
                    char_options = None
                    if character_filter:
                        should_proceed = character_filter.should_ignore_char(character)
                        if should_proceed == 1:
                            continue
                        if should_proceed == 0 and options:
                            char_options = options.get_options_for_char(character)
                    if program := mcfonts.utils.exporting.glyph_to_program(
                        resource.crop(
                            (
                                x_index * resolution[0],
                                y_index * resolution[1],
                                (x_index + 1) * resolution[0],
                                (y_index + 1) * resolution[1],
                            )
                        ),
                        -2,
                        125 / scale,
                        char_options,
                    ):
                        if character not in already_allocated_chars:
                            # Only allocate the character if it doesn't exist
                            mcfonts.utils.exporting.allocate_char(font_xml, character)
                            allocated_chars.append(character)
                        mcfonts.utils.exporting.set_program_to_char(
                            font_xml,
                            program,
                            character,
                            False,
                        )
        return set(allocated_chars)

    def validate(self) -> None:
        """
        Validate a "legacy_unicode" provider,
        ensuring its structure is correct and that all values are acceptable.

        .. warning:: This function does not validate textures.

        :returns: Nothing; problems are either raised or warned.
        """
        jsonschema.validate(self.contents, mcfonts.constants.SCHEMA_PROVIDER_LEGACY_UNICODE)

    def print_info(self) -> None:
        """
        Print information about this provider.
        """
        print(f"Template: {self.contents['template'] or mcfonts.constants.UNKNOWN_FIELD}")
        print(f"Sizes: {self.contents['sizes'] or mcfonts.constants.UNKNOWN_FIELD}")

    @staticmethod
    def to_advances(glyphsizes: bytes, match_unicode_category: list[str] | None = None) -> dict[str, int]:
        """
        Translate a glyphsizes.bin file into an "advances" mapping, which goes inside a "space"
        provider.

        .. warning:: This function does not return a new provider.

        :param glyphsizes: The bytes of glyphsizes.bin.
        :param match_unicode_category: Only translate Unicode characters with these categories.
            By default, this is [Mc, Zp, Zs, Zl].
            This should cover most whitespace and marking characters.
        :returns: An "advances" dictionary.
        """
        if match_unicode_category is None:
            match_unicode_category = ["Mc", "Zp", "Zs", "Zl"]
        advances = {}
        for index, nibble in enumerate(glyphsizes):
            if unicodedata.category(char := chr(index)) in match_unicode_category:
                advances[char] = (nibble & 0xF) - (nibble >> 4 & 0xF)
        return advances


AnyProvider = typing.TypeVar("AnyProvider", bound=Provider)
"""
A TypeVar for any kind of Provider subclass.
This includes :class:`OptionsProvider`.
"""
AnyVanillaProvider = typing.TypeVar(
    "AnyVanillaProvider", BitmapProvider, SpaceProvider, LegacyUnicodeProvider, TTFProvider
)
"""
A TypeVar for any kind of Provider subclass that the Vanilla game accepts.
This does not include :class:`OptionsProvider`.
"""


class ProviderFilter:
    """
    A provider filter, for use in :meth:`mcfonts.MinecraftFont.export`.
    These control what providers are exported, and on what conditions.
    """

    def __init__(
        self,
        select_providers: set[typing.Type[AnyVanillaProvider]] | None = None,
        providers_policy: typing.Literal["include", "exclude"] = "include",
    ):
        """
        :param select_providers:
            A set of Vanilla providers that will be either included or excluded from the exported font.
            For how to control this selection's effect, see `providers_policy`.

            If this is None, and `providers_policy` is "exclude", it will be set to:
                {mcfonts.providers.LegacyUnicodeProvider, mcfonts.providers.TTFProvider}
            If this is None and `providers_policy is "include", **it will be ignored**,
                regardless of what `providers_policy` is.
            An empty set will work as normal; the above is for None specifically.
        :param providers_policy:
            How to handle `select_providers`.

            * "include": Only these providers will be included
            * "exclude": These providers will not be exported
        """
        if select_providers is None and providers_policy == "exclude":
            select_providers = {mcfonts.providers.LegacyUnicodeProvider, mcfonts.providers.TTFProvider}
        self.select_providers: set[typing.Type[mcfonts.providers.AnyVanillaProvider]] | None = select_providers
        self.providers_policy: typing.Literal["include", "exclude"] = providers_policy

    def should_ignore_provider(self, provider: typing.Type[AnyVanillaProvider]) -> int:
        """
        Determine how to handle `provider`.
        Returns an integer describing how to proceed.

        :param provider: A class of :class:`mcfonts.providers.AnyVanillaProvider`. **Not an instance**.
        :returns:
            An integer describing how to proceed:

            0: Proceed as normal
            1: Ignore this provider
        """
        if self.select_providers and (
            (provider in self.select_providers and self.providers_policy == "exclude")
            or (provider not in self.select_providers and self.providers_policy == "include")
        ):
            return 1
        return 0


AnyFilter = typing.TypeVar("AnyFilter", CharacterFilter, ProviderFilter)
"""
A TypeVar for any kind of filter.
Includes :class:`CharacterFilter` and :class:`ProviderFilter`.
"""


def build_provider_list(
    providers: list[dict],
    resources: dict[str, PIL.Image.Image | bytes] | None = None,
    strict: bool = True,
) -> list[AnyProvider]:
    """
    Given a list of provider dictionaries, return a list of the appropriate :class:`Provider` classes.

    If an unknown provider is encountered, *it will not* be included.

    :param providers: A list of dictionaries that are individual providers.
    :param resources: A dictionary of {file name: :class:`PIL.Image.Image`}.
    :param strict:
        If a provider has bad data,
        an exception will be raised and no provider list will be returned if this is True.
        If this is False, None will be put in its place.
    :returns: A list of :class:`Provider` equivalents.
    :raises FileNotFoundError: If `strict` and a file is missing.
    :raises jsonschema.ValidationError: If `strict` and a provider structure is invalid
    """
    result: list[AnyProvider] = []
    if resources is None:
        resources = {}
    options = {}
    for provider in providers:
        try:
            if (provider_type := provider.get("type", "")).lower() == "bitmap":
                result.append(BitmapProvider(provider, resources.get(provider.get("file"))))
            elif provider_type == "space":
                result.append(SpaceProvider(provider))
            elif provider_type == "ttf":
                result.append(TTFProvider(provider, resources.get(provider.get("file"))))
            elif provider_type == "legacy_unicode":
                result.append(LegacyUnicodeProvider(provider, resources))
            elif provider_type in ("options", "mcfonts:options"):
                options = provider
        except (FileNotFoundError, jsonschema.ValidationError) as exception:
            if strict:
                raise exception
            continue
    try:
        if options:
            result.append(OptionsProvider(options))
    except jsonschema.ValidationError as exception:
        if strict:
            raise exception
    return result


def get_char_glyph_from_providers(
    providers: list[BitmapProvider],
    char: str,
) -> PIL.Image.Image | None:
    """
    Extract a desired character's glyph image from a list of :class:`mcfonts.providers.BitmapProvider`.

    Glyph textures that are mapped to spaces or null padding return None.
    If there is more than one sheet mapped to a character (duplicate characters),
    the first occurance will be returned.

    .. warning::
        This method is not efficient. Do not use it repeatedly,
        use :func:`get_glyphs_from_providers` and get each glyph from there.

    :param providers: The list of "bitmap" providers.
    :param char: A single character.
    :returns: A :class:`PIL.Image.Image`, or None if no glyph exists.
    """
    for provider in providers:
        if isinstance(provider, mcfonts.providers.BitmapProvider) and (glyph := provider.get_glyph_for_char(char)):
            return glyph
    return None


def format_provider_message(provider: AnyProvider | dict, message: str) -> str:
    """
    Format a provider warning message properly, following Provider <type>: <message>.

    Calls :func:`mcfonts.utils.pretty_print_provider()`.

    :param provider:
        The provider, either as a dictionary or instance of :data:`mcfonts.providers.AnyProvider`.
    :param message: The message to append at the end.
    :returns: The formatted warning message.
    """
    if isinstance(provider, dict):
        return f"Provider {pretty_print_provider_dictionary(provider)} {message}"
    return f"Provider {pretty_print_provider(provider)} {message}"


def pretty_print_provider(provider: AnyProvider) -> str:
    """
    Format a provider information message properly, following ``<type>`` plus:
     * ``bitmap``: ``<file> h <height> a <ascent>``
     * ``space``: nothing
     * ``legacy_unicode``: ``<template>``
     * ``ttf``: ``<file> s <shift0, 1>, sz <size>, o <oversample>, sk <skip>``

    :param provider:
        The provider as an instance of :data:`mcfonts.providers.AnyProvider`,
        or as a dictionary.
    :returns: The pretty provider information.
    """
    if isinstance(provider, BitmapProvider):
        return f"\"bitmap\": {provider.contents.get('file', 'no resource')}"
    if isinstance(provider, SpaceProvider):
        return '"space"'
    if isinstance(provider, LegacyUnicodeProvider):
        return f'"legacy_unicode": {provider.contents.get("template", "no template")}'
    if isinstance(provider, TTFProvider):
        return f'"ttf": {provider.contents.get("file", "no file")}'
    if isinstance(provider, OptionsProvider):
        return f'"options": {len(provider.chars_covered)} chars'
    return f'"{provider.provider_type}":'


def pretty_print_provider_dictionary(provider: dict) -> str:
    """
    Format a provider information message properly, following ``<type>`` plus:
     * ``bitmap``: ``<file> h <height> a <ascent>``
     * ``space``: nothing
     * ``legacy_unicode``: ``<template>``
     * ``ttf``: ``<file> s <shift0, 1>, sz <size>, o <oversample>, sk <skip>``

    :param provider:
        The provider as a dictionary,
        not an instance of :data:`mcfonts.providers.AnyProvider`.
    :returns: The pretty provider information.
    """
    if (provider_type := provider.get("type", "")).lower() == "bitmap":
        return f'"bitmap": {provider.get("file") or "no resource"}'
    if provider_type == "space":
        return '"space"'
    if provider_type == "legacy_unicode":
        return f'"legacy_unicode": {provider.get("template") or "no template"}'
    if provider_type == "ttf":
        return (
            f'"ttf": {provider.get("file", "no file")}, s '
            f'{provider.get("shift", "[?, ?]")}, sz '
            f'{provider.get("size", "?")}, o '
            f'{provider.get("oversample", "?")}, sk '
            f'{provider.get("skip", "none")}'
        )
    if provider_type == "options":
        return '"options"'
    return f'provider "{provider_type}": ?'
