# pylint: disable=all

import sys
import inspect
import logging
import asyncio
import traceback
from . import Retry, Context
from retry import retry


logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.DEBUG)


def decode_error(error: Exception) -> None:
    for frame, _ in traceback.walk_tb(error.__traceback__):
        print(" --> ", frame)
        for summary in traceback.extract_stack(frame):
            print(summary.filename)


def john_doe(x: list[int] = list(range(5))) -> bool:
    try:
        print(x.pop(0))
        raise ValueError(f"haha {len(x)}")
    except IndexError:
        return True

if __name__ == "__main__":
    RETRY = Retry(context=Context(tries=10, delay=1))
    albert = RETRY(john_doe)
    john = retry(tries=2)(john_doe)

    for func in (john_doe, john, albert):
        print(inspect.getfullargspec(func))
    assert inspect.getfullargspec(john) == inspect.getfullargspec(john_doe)
    assert inspect.getfullargspec(john) == inspect.getfullargspec(albert)

    import sys
    sys.exit(0)
    try:
        # asyncio.run(albert())
        pass
    except ValueError as error:
        decode_error(error)

    try:
        john()
    except ValueError as error:
        decode_error(error)
        raise
