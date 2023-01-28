import time
from typing import Callable, Union


def speed_test(func: Callable, key="MS", *args, **kwargs) -> Union[int, float]:
    """
    Taking a function to run.
    Additional taking a key(str) (MS = milliseconds, NS = nanoseconds)
    MS is preferred, because nanoseconds may not work on different OS.
    Returning result in <float>type or None-type object if key is invalid.
    :param func:  - function to run
    :param key: - MS(), NS(). MS - Default
    :return: float or None(if key is invalid).
    """
    if key == "MS":
        start_mark = time.monotonic()
        func()
        stop_mark = time.monotonic()
        runtime_mark = stop_mark - start_mark
        return runtime_mark
    elif key == "NS":
        start_mark = time.monotonic_ns()
        func()
        stop_mark = time.monotonic_ns()
        runtime_mark = stop_mark - start_mark
        return runtime_mark
