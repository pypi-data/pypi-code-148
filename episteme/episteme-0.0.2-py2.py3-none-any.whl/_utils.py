from __future__ import annotations

from typing import Any

from ulid import ULID


def dset(d: dict, k: str, v: Any):
    k = k.split('.')
    prev = tmp = d
    for i in k:
        if i not in tmp:
            tmp[i] = {}
        prev = tmp
        tmp = tmp[i]
    prev[i] = v


def dget(d: dict, k: str, default=None) -> Any:
    k = k.split('.')
    tmp = d
    for i in k:
        if i not in tmp:
            return default
        tmp = tmp[i]
    return tmp


def ulid() -> str:
    return str(ULID())
