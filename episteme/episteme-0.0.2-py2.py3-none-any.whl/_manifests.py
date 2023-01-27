from __future__ import annotations

import functools
from typing import final

from episteme._utils import dget


@final
class _Manifests:
    _manifests = {}

    def update(self, manifests):
        self._manifests = manifests

    def fetch(self, key=None):
        if key is None:
            return self._manifests
        else:
            return dget(self._manifests, key)


@functools.lru_cache(maxsize=1)
def get_manifests():
    return _Manifests()
