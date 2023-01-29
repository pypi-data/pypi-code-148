"""@Author Rayane AMROUCHE

Logger Class.
"""

import os
import logging
import inspect
import datetime
import functools

from typing import Any, Optional

from dsmanager.controller.config import Config
from dsmanager.controller.utils import i_display


class Logger:
    """Logger class."""

    logger_alias = {}  # type: dict

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> logging.Logger:
        """Wrap getLogger function from logging.

        Args:
            name (str): Name of the logger to get.

        Returns:
            logging.Logger: Returns the required logger.
        """
        if not name:
            raise ValueError("Missing a logger name.")
        if name not in cls.logger_alias:
            return logging.Logger.manager.getLogger(name)
        return logging.Logger.manager.getLogger(cls.logger_alias[name])

    @staticmethod
    def log_func(logger_name: Any):
        """Decorate a function to log it.

        Args:
            logger (Any): Name of the logger to use.

        Returns:
            Any: Output of the function decorated.
        """

        logger = Logger.get_logger(logger_name)

        def decorator(func: Any) -> Any:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                tic = datetime.datetime.now()
                result = None
                raise_err = False
                try:
                    result = func(*args, **kwargs)
                except Exception as err:  # pylint: disable=broad-except
                    result = err
                    raise_err = True
                time_taken = str(datetime.datetime.now() - tic)
                res_repr, displ = i_display(result)
                msg = (
                    f"Executed '{func.__qualname__}' in {time_taken}s; "
                    f"Output: {result.__class__.__name__ + ': ' if raise_err else ''}"
                    f"{res_repr}"
                )
                if raise_err:
                    logger.warning(msg)
                    raise result
                logger.info(msg)
                displ()
                return result

            return wrapper

        return decorator

    @classmethod
    def update_logger(
        cls,
        name: str,
        path: Any = None,
        verbose: Any = None,
        logger: Any = None,
    ) -> None:
        """Update a logging logger.

        Args:
            name (str): Name of the logger.
            path (str): Logging file path.
            verbose (int, optional): Verbose level. Defaults to 0.
            logger (Any, optional): Default logger inherited to avoid duplication.
                Defaults to Any.

        Returns:
            logging.Logger: Logging logger generated.
        """
        if logger is None:
            logger = logging.getLogger(name)
        cls.logger_alias[name] = logger.name
        cls.logger_alias[logger.name] = logger.name

        handlers = logger.handlers[:]
        for handler in handlers:
            logger.removeHandler(handler)
            handler.close()
        logger.setLevel(logging.INFO)

        if not path:
            path = Config.get_option("logger_path")
        if not verbose:
            verbose = Config.get_option("logger_verbose")

        if path and verbose > 0:
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%a, %d %b %Y %H:%M:%S",
            )
            os.makedirs(path, exist_ok=True)
            file_handler = logging.FileHandler(os.path.join(path, name + ".log"))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            global_handler = logging.FileHandler(os.path.join(path, "all.log"))
            global_handler.setFormatter(formatter)
            logger.addHandler(global_handler)

        if verbose > 1:
            console_handler = logging.StreamHandler()
            logger.addHandler(console_handler)

    @staticmethod
    def log_source(datasource_mode: str, info_to_show: list) -> Any:
        """Log dataSources data loading.
        Args:
            datasource_mode (str): Can be either "read" or "write".
            info_to_show (list): Source informations to log.

        Raises:
            err: Raise an exception if an exception is caught.

        Returns:
            Any: Return a decorator to log a given function.
        """

        if datasource_mode == "read":
            action = "Extract data from"
        else:
            action = "Load data to"

        def decorator(func):
            source_name = func.__qualname__.split(".")[0]

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                bind_func = inspect.signature(func).bind(*args, **kwargs)
                bind_func.apply_defaults()
                callargs = bind_func.arguments
                params = ", ".join(
                    [f"{param}={callargs[param]}" for param in info_to_show]
                )
                try:
                    result = func(*args, **kwargs)
                except Exception as err:  # pylint: disable=broad-except
                    Logger.get_logger("datasource").warning(
                        "Failed to %s %s(%s).", action.lower(), source_name, params
                    )
                    raise err
                Logger.get_logger("datasource").info(
                    "%s %s(%s).", action, source_name, params
                )
                return result

            return wrapper

        return decorator
