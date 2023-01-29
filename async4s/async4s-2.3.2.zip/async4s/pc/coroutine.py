#!/usr/bin/env python

"""
Producer-Consumer模型-协程实现方式
"""

from __future__ import annotations

import asyncio
import abc
from typing import Type


class Runnable(metaclass=abc.ABCMeta):
    def __init__(self, buffer: asyncio.Queue):
        self._buffer = buffer

    @abc.abstractmethod
    async def run(self):
        pass

    @property
    def buffer(self):
        return self._buffer


class Producer(Runnable):
    pass


class Consumer(Runnable):
    pass


class Manager(object):
    def __init__(self, producer_cls: Type[Producer], producer_cnt: int, consumer_cls: Type[Consumer], consumer_cnt: int, buffer_size=1024):
        self._buffer = self._create_buffer(buffer_size)
        self._producer_cls = producer_cls
        self._producer_cnt = producer_cnt
        self._consumer_cls = consumer_cls
        self._consumer_cnt = consumer_cnt
    
    def _create_buffer(self, buffer_size=1024):
        return asyncio.Queue(buffer_size)

    async def start(self, loop=None):
        tasks = []
        for _ in range(self._producer_cnt):
            tasks.append(asyncio.ensure_future(self._producer_cls(self._buffer).run()))
        for _ in range(self._consumer_cnt):
            tasks.append(asyncio.ensure_future(self._consumer_cls(self._buffer).run()))
        return await asyncio.gather(*tasks, loop=loop)

    @property
    def buffer(self):
        return self._buffer
