import typing
import warnings

from ._is_in_coverage_run import is_in_coverage_run


def jit(*args, **kwargs) -> typing.Callable:
    """Decorator that performs jit compilation if numba available.

    Disables jit during coverage measurement to increase source
    visibility.
    """
    try:
        import numba as nb
    except ModuleNotFoundError:
        warnings.warn(
            "numba unavailable,"
            "wrapped function may lose significant performance",
            ImportWarning,
        )
        return lambda f: f

    if is_in_coverage_run():
        warnings.warn(
            "code coverage tracing detected,"
            "disabling jit compilation to increase source visibility",
            RuntimeWarning,
        )
        return lambda f: f
    else:
        return nb.jit(*args, **kwargs)
