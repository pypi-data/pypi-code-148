"""
Hoppr utility functions
"""
from __future__ import annotations

import importlib
import inspect

from pathlib import Path
from typing import Any

import yaml

from yaml.parser import ParserError as YAMLParserError
from yaml.scanner import ScannerError as YAMLScannerError

from hoppr.context import Context
from hoppr.exceptions import HopprLoadDataError, HopprPluginError


def _class_in_module(obj, module):
    """
    Determines if the specified object is a class
    defined in the module
    """
    if not inspect.isclass(obj):
        return False

    module_source_string = inspect.getsource(module)
    class_source_string = inspect.getsource(obj)

    if class_source_string not in module_source_string:
        return False

    return True


def plugin_class(plugin_name):
    """
    return a concrete class of an object defined by a plugin name

    Assumes the specified plugin will define exactly one concrete class, which
    will be instaniated using a default constructor (i.e., one with no parameters).
    """
    try:
        plugin = importlib.import_module(plugin_name)
    except ModuleNotFoundError as mnfe:
        raise ModuleNotFoundError(f"Unable to locate plug-in {plugin_name}: {mnfe}") from mnfe

    plugin_cls = None

    for name, obj in inspect.getmembers(plugin):
        if _class_in_module(obj, plugin):

            if plugin_cls is not None:
                raise HopprPluginError(
                    f"Multiple candidate classes defined in {plugin_name}: " + f"{plugin_cls.__name__}, {name}"
                )

            plugin_cls = obj

    if plugin_cls is None:
        raise HopprPluginError(f"No class definition found in in {plugin_name}.")

    return plugin_cls


def plugin_instance(plugin_name: str, context: Context, config: Any = None):
    """
    Create an instance of an object defined by a plugin name

    Assumes the specified plugin will define exactly one concrete class, which
    will be instaniated using a default constructor (i.e., one with no parameters).
    """
    plugin_cls = plugin_class(plugin_name)

    return plugin_cls(context=context, config=config)


def load_string(contents: str) -> dict | list | None:
    """
    Return a YAML or JSON formatted string as a dict
    """
    if not contents.strip():
        raise HopprLoadDataError("Empty string cannot be parsed.")

    # Replace tab characters with spaces to prevent parsing errors
    contents = contents.replace("\t", "  ")
    loaded_contents: dict | list | None = None

    try:
        # Applicable to both YAML and JSON formats since valid JSON data is also valid YAML
        loaded_contents = yaml.safe_load(contents)

        # yaml.safe_load will sometimes return a single string rather than the required structure
        if isinstance(loaded_contents, str):
            raise HopprLoadDataError("Expected dictionary or list, but contents were loaded and returned as string")
    except (YAMLParserError, YAMLScannerError) as ex:
        raise HopprLoadDataError("Unable to recognize data as either json or yaml") from ex
    except HopprLoadDataError as ex:
        raise HopprLoadDataError from ex

    return loaded_contents


def load_file(input_file_path: Path) -> dict | list | None:
    """
    Load file content (either JSON or YAML) into a dict
    """

    if not input_file_path.is_file():
        raise HopprLoadDataError(f"{input_file_path} is not a file, cannot be opened.")

    with input_file_path.open(mode="r", encoding="utf-8") as input_file:
        content: str = input_file.read()
        if not content.strip():
            raise HopprLoadDataError(f"File {input_file_path} is empty.")

    return load_string(content)


def dedup_list(list_in: list[Any]) -> list[Any]:
    """
    De-duplicate a list
    """
    return list(dict.fromkeys(list_in)) if list_in is not None else []


def obscure_passwords(command_list, lst):
    """
    Returns an input string with any specified passwords hidden
    """

    command = ""
    for arg in command_list:
        if len(command) > 0:
            command += " "
        if " " in arg:
            command += f'"{arg}"'
        else:
            command += arg

    if lst is not None:
        for password in lst:
            if password is not None:
                command = command.replace(password, "<PASSWORD HIDDEN>")

    return command


def remove_empty(directory: Path) -> set[Path]:
    """
    Removes empty folders given the directory including parent folders
    """
    deleted = set()

    if not directory.exists():
        raise FileNotFoundError()

    for subdir in directory.iterdir():
        if subdir.is_dir():
            deleted.update(remove_empty(subdir))

    if directory.is_dir() and not any(directory.iterdir()):
        directory.rmdir()
        deleted.add(directory)

    return deleted
