# pylint: disable=all

import sys
import logging
import asyncio
from . import Retry, Context

logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.DEBUG)

if __name__ == "__main__":
    RETRY = Retry(context=Context(tries=3, delay=1))
    print(RETRY)
    @RETRY
    async def albert(x: list[int] = list(range(5))) -> bool:
        try:
            print(x.pop(0))
            raise ValueError(f"haha {len(x)}")
        except IndexError:
            return True
    try:
        asyncio.run(albert())
    except ValueError:
        print("unsuccesful")
