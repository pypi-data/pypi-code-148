"""@Author Rayane AMROUCHE

Async tools.
"""
import functools
import asyncio

from typing import Any

from concurrent.futures import ThreadPoolExecutor

import nest_asyncio  # type: ignore


nest_asyncio.apply()


def force_async(func: Any) -> Any:
    """Turns a sync function to async function using threads.

    Args:
        func (Any): Function to wrap.

    Returns:
        Any: Function wrapped with async transparency.
    """

    pool = ThreadPoolExecutor()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = pool.submit(func, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(func: Any) -> Any:
    """Turn an async function to sync function.

    Args:
        func (Any): Function to wrap.

    Returns:
        Any: Function wrapped with sync transparency.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper
