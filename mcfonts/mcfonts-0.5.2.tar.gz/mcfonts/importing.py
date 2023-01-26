#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Functions to import fonts from both Java Edition and Bedrock Edition
in a variety of formats and configurations.

All of these return a :class:`mcfonts.MinecraftFont`.
"""
import json
import os
import shutil
import tempfile
import zipfile

import mcfonts.constants
import mcfonts.providers
import mcfonts.utils.bitmap
import mcfonts.utils


def from_java_font_file(
    file_path: str,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition font JSON into a :class:`mcfonts.MinecraftFont`.
    Requires a "providers" list, and missing files will raise an error.

    :param file_path:
        The file path to the font JSON.
    :param read_colors:
        If True, glyph will be loaded in RGBA. If false, loaded in LA.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error
        * Missing files will raise an error

        If False:

        * Bad providers will be ignored
        * Missing files will be skipped
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    with open(file_path, encoding="utf-8") as datafp:
        file_contents: dict = json.load(datafp, strict=False)
    return from_java_font_contents(file_contents, file_path, read_colors, strict)


def from_java_font_contents(
    file_contents: dict,
    file_path: str,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition font JSON into a :class:`mcfonts.MinecraftFont`.
    Requires a "providers" list, and missing files will raise an error.

    :param file_contents:
        The contents of the font JSON file, loaded as a dictionary.
        This dictionary should include the base "providers" key.
    :param file_path:
        The file path to the font JSON.
        This is needed for loading resources.
    :param read_colors:
        If True, glyph will be loaded in RGBA. If false, loaded in LA.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error
        * Missing files will raise an error

        If False:

        * Bad providers will be ignored
        * Missing files will be skipped
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    provider_content = file_contents.get("providers", [])
    if read_colors:
        mode = "RGBA"
    else:
        mode = "LA"
    return mcfonts.MinecraftFont(
        mcfonts.providers.build_provider_list(
            provider_content,
            mcfonts.utils.bitmap.load_resources(provider_content, mcfonts.utils.expand_path(file_path), strict, mode),
            strict,
        )
    )


def from_java_pack_folder(
    folder_path: str,
    font_file_name: str = "default.json",
    namespace: str = "minecraft",
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition resource pack into a :class:`mcfonts.MinecraftFont`.
    The font must be in the path ``assets/<namespace>/font/<fontfile>``.

    :param folder_path:
        The path to the folder that contains a resource pack.
        This is not the ``assets`` folder, nor is it a ZIP file.
        The files inside this folder should be ``assets/``, and ``pack.mcmeta``.
    :param font_file_name:
        The name of the font file.
        By default, this is "default.json".
    :param namespace:
        The namespace to find assets in.
        By default, this is "minecraft".
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error
        * Missing files will raise an error

        If False:

        * Bad providers will be ignored
        * Missing files will be skipped
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    return from_java_font_file(
        os.path.join(
            mcfonts.utils.expand_path(folder_path),
            f"assets/{namespace}/font/{font_file_name}",
        ),
        read_colors,
        strict,
    )


def from_java_pack_zip(
    file_path: str, password: bytes | None = None, read_colors: bool = False, strict: bool = True
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition resource pack ZIP into a :class:`mcfonts.MinecraftFont`.
    The font must be in the path ``assets/<namespace>/font/<fontfile>``.

    :param file_path:
        The path to the ZIP file.
    :param password:
        Password to use when reading the ZIP file.
        Set to ``None`` if there is no password.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error
        * Missing files will raise an error

        If False:

        * Bad providers will be ignored
        * Missing files will be skipped
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(mcfonts.utils.expand_path(file_path)) as zip_file:
            zip_file.extractall(temp_dir, pwd=password)
        return from_java_pack_folder(temp_dir, read_colors=read_colors, strict=strict)


def from_java_resource_template(
    file_path: str,
    template_provider: dict | None = None,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Given the path to a texture and the contents of an individual font provider,
    return a :class:`mcfonts.MinecraftFont` instance with it and the resource in `file_path`.

    ``template_provider["file"]`` can be any value, it will be overwritten anyway,
    although it must exist.

    :param file_path:
        The path to the PNG :term:`resource` that needs templating.
    :param template_provider:
        An individual provider dictionary.
        Not a list of providers.
        By default, this is :const:`mcfonts.utils.templates.PROVIDER_ASCII`.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If a provider has bad data,
        an exception will be raised and no provider list will be returned if this is True.
        If this is False, it will be ignored.
    :returns:
        A :class:`mcfonts.MinecraftFont` instance.
    """
    if template_provider is None:
        template_provider = mcfonts.constants.PROVIDER_ASCII
    # Make a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Put the PNG file into the temp dir to later read all-together
        shutil.copy(file_path := mcfonts.utils.expand_path(file_path), temp_dir)
        # Make a temporary fake provider file
        with tempfile.NamedTemporaryFile("w+", dir=temp_dir) as temp_file:
            # Overwrite default file, use expanded argument with modifications
            try:
                template_provider["file"] = mcfonts.utils.expand_resource_location(file_path)
            except KeyError as exception:
                if strict:
                    raise exception
            json.dump(template_provider, temp_file, ensure_ascii=False)
        return from_java_font_file(temp_file.name, read_colors, strict)


def from_java_ambiguous(path: str, read_colors: bool = False, strict: bool = True) -> mcfonts.MinecraftFont:
    """
    For file paths where the file pointed to is of an unknown type:
    it could be a JSON, ZIP, or directory.

    This function automatically figures out which function to use, and returns a MinecraftFont.


    :param path:
        The path to either a file or a folder.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error
        * Missing files will raise an error

        If False:

        * Bad providers will be ignored
        * Missing files will be skipped
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    """
    if path.endswith(".json"):
        return from_java_font_file(path, read_colors, strict)
    if os.path.isdir(path):
        return from_java_pack_folder(path, read_colors=read_colors, strict=strict)
    # Not a JSON, not a directory, must be a ZIP.
    return from_java_pack_zip(path, read_colors=read_colors, strict=strict)
