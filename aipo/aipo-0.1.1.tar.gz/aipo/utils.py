import asyncio
import importlib
from functools import partial
from typing import Any, Callable, Dict, Tuple


def get_fully_qualified_name(obj: Any) -> str:
    """Get fully qualified name of an object.
    E.g. aipo.app.AipoApp

    :param obj: The object to get the fully qualified name of

    :return: The fully qualified name of the object
    """
    return f"{obj.__module__}.{obj.__name__}"


async def ensure_async(func: Callable, *args: Tuple, **kwargs: Dict) -> Any:
    """Ensure that a function is executed asynchronously.
    If the function is a coroutine, it will be awaited.
    If the function is not a coroutine, it will be executed in the loop's executor.

    :param func: The function to execute
    :param args: The positional arguments to pass to the function
    :param kwargs: The keyword arguments to pass to the function

    :return: The result of the function
    """
    if asyncio.iscoroutinefunction(func):
        return await asyncio.create_task(func(*args, **kwargs))
    else:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))


def import_from_string(import_path: str) -> Any:
    """Import an object from a string.
    E.g. aipo.app.AipoApp

    :param import_path: The string to import from

    :return: The imported object
    """
    module_path, _, object_name = import_path.rpartition(".")
    module = importlib.import_module(module_path)
    return getattr(module, object_name)
