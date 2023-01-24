"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import logging
import time
from copy import deepcopy

_logger = logging.getLogger(__name__)

class TTLCache(object):
    """In memory cache implementation with TTL support.
    Items are expired and popped during mutating operations instead of using periodic checks."""

    _cache = {}
    _ttl = 300  # in seconds, defaults to 5 minutes

    def __init__(self, ttl):
        self._ttl = ttl
        _logger.debug("TTLCache init complete")

    def _check_ttls(self):
        """
        Cycles through all cached items and pops the ones that are expired
        """
        now = time.time()
        to_pop = []
        # build a list of expired keys
        for key in self._cache:
            item = self._cache.get(key)
            if item.get("exp") < now:
                to_pop.append(key)
        # remove the expired keys from the cache
        for key in to_pop:
            self._cache.pop(key, None)

    def set(self, key, value, ttl=_ttl):
        """
        Set a key/value pair in the cache with a specific ttl in seconds (or the default one)
        @param key      {str}
        @param value    {any}
        @param ttl      {int}   Time to live in seconds
        """
        self._check_ttls()
        self._cache[key] = {"exp": time.time() + ttl, "value": value}

    def get(self, key):
        """
        Get a cached value using its key
        @param key      {str}
        @returns {any}
        """
        self._check_ttls()
        return deepcopy(self._cache.get(key).get("value")) if self._cache.get(key) else None

    def pop(self, key):
        """
        Remove an item from the cache using its key
        @param key      {str}
        """
        self._check_ttls()
        self._cache.pop(key, None)

    def clear(self):
        """
        Clears the cache i.e. removes all saved items
        """
        self._cache = {}
