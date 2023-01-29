"""@Author Rayane AMROUCHE

Config Class.
"""

import warnings

from typing import Type, Any, TypeVar, Generic, Optional

import pandas as pd  # type: ignore

T = TypeVar("T")


class Option(Generic[T]):
    """Option Class to allow resettable attributes."""

    def __init__(self, default_value: T) -> None:
        # the attribute stores the default value
        self.default_value = default_value
        # and its name (will be filled later)
        self.name = ""

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        # this method is called when we instantiate a descriptor inside a class
        # prepend an underscore to prevent name collisions
        self.name = f"_{name}"

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> T:
        # this is called when we access the descriptor from a class (or instance)
        # return the stored value or the default if it was never set
        return getattr(instance, self.name, self.default_value)

    def __set__(self, instance: Any, value: T) -> None:
        # this is called when we assign to the descriptor from an instance
        setattr(instance, self.name, value)

    def __delete__(self, instance: Any) -> None:
        # this is called when you write del instance.attribute
        # we can use this to reset the value to the default
        setattr(instance, self.name, self.default_value)

    def __repr__(self) -> str:
        return repr(getattr(None, self.name, self.default_value))


class ConfigUtils: #pylint: disable=too-few-public-methodsƒ
    """Utils for the Config class"""

    @staticmethod
    def setup_notebook() -> None:
        """Setup some notebook parameters."""
        pd.set_option("display.max_columns", None)
        pd.set_option("display.expand_frame_repr", False)

        def warn(*args, **kwargs):  # pylint: disable=unused-argument
            pass

        warnings.warn = warn


class Config:
    """Config class to keep track of a set of options."""

    logger_path: Option[Any] = Option("/tmp/logs")
    logger_verbose: Option[int] = Option(2)
    env_path: Any = Option(None)

    utils = ConfigUtils()

    @classmethod
    def set_option(cls, __name: str, __value: Any) -> None:
        """Set option to config as an attributes.

        Args:
            __name (str): Name of the option.
            __value (Any): Value of the option.
        """
        setattr(cls, __name, __value)

    @classmethod
    def get_option(cls, __name: str) -> Any:
        """Get an option value.

        Args:
            __name (str): Name of the option.

        Returns:
            Any: Value of the selected option.
        """
        return getattr(cls, __name)

    @classmethod
    def reset_option(cls, __name: str) -> None:
        """Reset an option.

        Args:
            __name (str): Name of the option.
        """
        delattr(cls, __name)

    @classmethod
    def print_options(cls) -> None:
        """Print the list of options."""
        list_of_options = dir(cls)
        res_print = ""
        for option in list_of_options:
            if option in [
                "utils",
                "set_option",
                "get_option",
                "reset_option",
                "print_options",
            ]:
                continue
            if option.startswith("__"):
                continue
            res_print += f"{option} = {repr(cls.__dict__[option])}\n"
        print(res_print)

    @classmethod
    def __setattr__(cls, __name: str, __value: Any) -> None:
        cls.set_option(__name, __value)
