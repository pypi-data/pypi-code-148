import inspect
import logging
from functools import partial, wraps
from typing import Any, Callable, Optional, TypeVar, Union, overload

R = TypeVar("R")
F = TypeVar("F", bound=Callable[..., Any])


@overload
def log(func: F) -> F:
    ...


@overload
def log(
    *,
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
    stacklevel: int = 2,
    nested: bool = False,
) -> Callable[[F], F]:
    ...


def log(
    func: Optional[Callable[..., R]] = None,
    *,
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
    stacklevel: int = 2,
    nested: bool = False,
) -> Union[Callable[[Callable[..., R]], Callable[..., R]], Callable[..., R]]:
    def get_caller_info(func: Callable[..., R]) -> dict[str, Any]:
        try:
            real_func = inspect.unwrap(func)
            if real_func is None:
                real_func = func
        except ValueError:
            real_func = func
        if real_func:
            return {
                "filename": real_func.__code__.co_filename,
                "lineno": real_func.__code__.co_firstlineno,
            }
        return {}

    def wrapper(func: Callable[..., R], *args: Any, **kwargs: Any) -> R:
        nonlocal logger
        if logger is None:
            logger = logging.getLogger(func.__module__)

        args_repr = list(map(repr, args))
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        caller_info = {"caller_info": get_caller_info(func)} if nested else {}

        try:
            result = func(*args, **kwargs)
        except Exception as exp:
            logger.log(
                level,
                "Function %s called with args: (%s), raised exception.",
                func.__name__,
                signature,
                exc_info=exp,
                stacklevel=stacklevel,
                extra=caller_info,
            )
            raise exp
        else:
            logger.log(
                level,
                "Function %s called with args: (%s), returned: %r.",
                func.__name__,
                signature,
                result,
                stacklevel=stacklevel,
                extra=caller_info,
            )
            return result

    if func is not None:
        if callable(func):
            return wraps(func)(partial(wrapper, func))
        raise TypeError(f"{func!r} is not a callable.")

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        return wraps(func)(partial(wrapper, func))

    return decorator
