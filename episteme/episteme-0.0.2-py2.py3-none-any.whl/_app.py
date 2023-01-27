from __future__ import annotations

import functools
from typing import final

from episteme._manifests import get_manifests


def get_schema():
    return get_manifests().fetch('models')


db = {}

m = get_manifests()


@final
class _App:
    def __init__(self) -> None:
        pass

    def get_all(self):
        return m.fetch('app').keys()


@functools.lru_cache(maxsize=1)
def app():
    return _App()
