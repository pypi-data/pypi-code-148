"""Logging."""
from contextlib import asynccontextmanager as _asynccontextmanager
from contextvars import ContextVar as _ContextVar
from typing import (
    Any as _Any,
    Dict as _Dict,
    Callable as _Callable,
    Coroutine as _Coroutine,
    AsyncGenerator as _AsyncGenerator,
    Optional as _Optional,
)
from time import perf_counter as _perf_counter

context_log: _ContextVar[_Dict[str, _Any]] = _ContextVar("context_log")

_DEFAULT_LOG: _Dict[str, _Any] = dict(level="info")


def get_logger() -> _Dict[str, _Any]:
    """Get the current request logger.

    Returns:
        Log dict.
    """
    return context_log.get()


@_asynccontextmanager
async def logger(
    server: _Optional[str],
    emit_log: _Callable[[_Dict[str, _Any]], _Coroutine[None, None, None]],
) -> _AsyncGenerator[_Dict[str, _Any], None]:
    """Logger context manager.

    Args:
        server: Server ID.
        emit_log: Async function to use to emit logs.

    Returns:
        Logger.
    """
    start = _perf_counter()

    # Keep the same value for server if lambda reuse the same cached function
    if server:
        _DEFAULT_LOG.setdefault("server", server)

    log = _DEFAULT_LOG.copy()
    context_log.set(log)

    try:
        yield log
    finally:
        log["execution_time_ms"] = round((_perf_counter() - start) * 1e3, 1)
        await emit_log(log)
