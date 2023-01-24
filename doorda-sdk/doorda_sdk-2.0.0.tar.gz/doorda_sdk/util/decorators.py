import signal
from functools import wraps
import errno
import os
from doorda_sdk.util.exc import NotConnectedError
import warnings


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise NotConnectedError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def deprecated(reason):
    def decorator(func):
        def wrapper(*args, **kwargs):
            fmt = "`{name}` function will be deprecated ({reason})"
            warnings.simplefilter(
                "always", PendingDeprecationWarning
            )  # turn off filter
            warnings.warn(
                fmt.format(name=func.__name__, reason=reason),
                category=PendingDeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter(
                "default", PendingDeprecationWarning
            )  # reset filter
            result = func(*args, **kwargs)
            return result

        return wraps(func)(wrapper)

    return decorator
