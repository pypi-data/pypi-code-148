"""@Author: Rayane AMROUCHE

Utils functions for controller.
"""

import re
import os
import json
import pickle
import logging

from typing import Any, Tuple, Dict

from inspect import signature

import __main__ as main

from IPython.display import display  # type: ignore

from dsmanager.datamanager.datastorage import DataStorage
from dsmanager.controller.config import Config


def is_interactive() -> bool:
    """Check wether the code is runned on a notebook.

    Returns:
        bool: True if runned on notebook, else False.
    """
    return not hasattr(main, "__file__")


def i_display(str_: Any, max_len: int = 50) -> Any:
    """Display or return a given string depending on its length.

    Args:
        str_ (Any): String to display or return.
        max_len (int): Maximum length allowed for the string to be returned.

    Returns:
        str: Original string or {...} if the length is more than max_len as well as a
            display function to call if something has to be displayed.
    """

    def displ():
        return

    res_repr = "{...}"

    if len(repr(str_)) < max_len:
        res_repr = str_

    if Config.logger_verbose > 2:
        red = "\033[91m"
        italics = "\033[3m"
        underline = "\033[4m"
        end = "\033[0m"
        warning_msg = (
            red
            + underline
            + italics
            + "Result is displayed because the output is too long."
            + end
        )

        def print_res():
            logging.getLogger(None).warning(warning_msg)
            display(str_)

        displ = print_res

    return res_repr, displ


def json_to_dict(path: str) -> dict:
    """Read a json file as a dict.

    Args:
        path (str, optional): Path of the json file to transform as a python dict.

    Raises:
        FileNotFoundError: Raised if the file is not found.

    Returns:
        dict: Json file as a python dict.
    """
    # check if file exists
    if not os.path.exists(path):
        base_path = os.path.dirname(path)
        if base_path:
            os.makedirs(base_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as outfile:
            json.dump({}, outfile)

    # check if file is a json
    try:
        with open(path, encoding="utf-8") as json_file:
            file_dict = json.load(json_file, object_pairs_hook=DataStorage)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Given file is not a valid json. Details: {exc}") from exc
    return file_dict


def pickle_to_ds(path: str) -> Any:
    """Read a pickle file as a DataStorage.

    Args:
        path (str, optional): Path of the pickle file to transform as a DataStorage.

    Raises:
        FileNotFoundError: Raised if the file is not found.

    Returns:
        dict: Pickle file as a DataStorage.
    """
    # check if file exists
    if not os.path.exists(path):
        base_path = os.path.dirname(path)
        if base_path:
            os.makedirs(base_path, exist_ok=True)
        with open(path, "wb") as outfile:
            pickle.dump(DataStorage(), outfile)

    # check if file is a pickle
    try:
        with open(path, "rb") as infile:
            file_dict = pickle.load(infile)
    except pickle.UnpicklingError as exc:
        raise ValueError(f"Given file is not a valid pickle. Details: {exc}") from exc
    return file_dict


def format_dict(dico: dict, formatting: dict) -> None:
    """Read a json file as a dict.

    Args:
        dico (dict): Dict where keys have to be formated.
        formatting (dict): Formatting dictionary.

    """
    for key_, value_ in dico.items():
        if isinstance(value_, str) and any(k in value_ for k in formatting.keys()):
            dico[key_] = value_.format(**formatting)
        if isinstance(value_, dict):
            format_dict(value_, formatting)


def camel_to_snake(str_: str) -> str:
    """Transform a camel case name to a snake case one.

    Args:
        str_ (str): String to transform.

    Returns:
        str: Transformed string.
    """
    str_ = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str_)
    str_ = re.sub("([a-z0-9])([A-Z])", r"\1_\2", str_).lower()
    return re.sub("_+", "_", str_)


def remove_special(str_: str) -> str:
    """Transform special characters to their meaning or to space.

    Args:
        str_ (str): String to transform.

    Returns:
        str: Transformed string.
    """
    str_ = str_.replace("%", " Percent ")
    str_ = str_.replace("@", " At ")
    str_ = str_.replace("/w ", " With ")
    return re.sub(r"\W+", " ", str_)


def remove_spaces(str_: str) -> str:
    """Transform spaces to simple underscore.

    Args:
        str_ (str): String to transform.

    Returns:
        str: Transformed string.
    """
    str_ = re.sub(" +", " ", str_)
    str_ = str_.strip(" ")
    return str_.replace(" ", "_")


def fill_kwargs(func: Any, **kwargs: Any) -> dict:
    """Fill kwargs given the signature of a function.

    Args:
        func (Any): function to analyse.

    Returns:
        dict: Wwargs verified for func.
    """
    verified_kwargs = {}
    for key_, value_ in kwargs.items():
        if key_ in signature(func).parameters.keys():
            verified_kwargs[key_] = value_
    return verified_kwargs


def args_kwargs(*args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    """Get args and kwargs from args and kwargs.

    Returns:
        Tuple[Tuple[Any, ...], Dict[str, Any]]: Args and kwargs.
    """
    return args, kwargs
