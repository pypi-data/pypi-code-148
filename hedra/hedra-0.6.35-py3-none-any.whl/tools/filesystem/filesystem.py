
import asyncio
import sys

from io import (
    FileIO,
    TextIOBase,
    BufferedReader,
    BufferedWriter,
    BufferedRandom,
    BufferedIOBase,
)
from functools import partial, singledispatch

from .binary import (
    AsyncBufferedIOBase,
    AsyncBufferedReader,
    AsyncFileIO,
    AsyncIndirectBufferedIOBase
)
from .text import AsyncTextIOWrapper, AsyncTextIndirectIOWrapper


sync_open = open

__all__ = (
    "open",
    "stdin",
    "stdout",
    "stderr",
    "stdin_bytes",
    "stdout_bytes",
    "stderr_bytes",
)


async def open(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
    *,
    loop=None,
    executor=None
) -> AsyncTextIOWrapper:

    return await _open(
        file,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        closefd=closefd,
        opener=opener,
        loop=loop,
        executor=executor,
    )


async def _open(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
    *,
    loop=None,
    executor=None
):
    """Open an asyncio file."""
    if loop is None:
        loop = asyncio.get_event_loop()
    cb = partial(
        sync_open,
        file,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        closefd=closefd,
        opener=opener,
    )
    async_file = await loop.run_in_executor(executor, cb)

    return wrap(async_file, loop=loop, executor=executor)


@singledispatch
def wrap(file, *, loop=None, executor=None):
    raise TypeError("Unsupported io type: {}.".format(file))


@wrap.register(TextIOBase)
def _(file, *, loop=None, executor=None):
    return AsyncTextIOWrapper(file, loop=loop, executor=executor)


@wrap.register(BufferedWriter)
@wrap.register(BufferedIOBase)
def _(file, *, loop=None, executor=None):
    return AsyncBufferedIOBase(file, loop=loop, executor=executor)


@wrap.register(BufferedReader)
@wrap.register(BufferedRandom)
def _(file, *, loop=None, executor=None):
    return AsyncBufferedReader(file, loop=loop, executor=executor)


@wrap.register(FileIO)
def _(file, *, loop=None, executor=None):
    return AsyncFileIO(file, loop=loop, executor=executor)


stdin = AsyncTextIndirectIOWrapper('sys.stdin', None, None, indirect=lambda: sys.stdin)
stdout = AsyncTextIndirectIOWrapper('sys.stdout', None, None, indirect=lambda: sys.stdout)
stderr = AsyncTextIndirectIOWrapper('sys.stderr', None, None, indirect=lambda: sys.stderr)
stdin_bytes = AsyncIndirectBufferedIOBase('sys.stdin.buffer', None, None, indirect=lambda: sys.stdin.buffer)
stdout_bytes = AsyncIndirectBufferedIOBase('sys.stdout.buffer', None, None, indirect=lambda: sys.stdout.buffer)
stderr_bytes = AsyncIndirectBufferedIOBase('sys.stderr.buffer', None, None, indirect=lambda: sys.stderr.buffer)