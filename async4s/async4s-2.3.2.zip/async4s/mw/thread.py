#!/usr/bin/env python

"""
Master-Worker模型-多线程实现方式
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
import abc

__all__ = ["Master", "Worker"]

class Worker(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def done_callback(self, result: Future):
        pass


class Master(object):
    def __init__(self, max_workers: int = None):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def start(self, worker: Worker):
        self._executor.submit(worker.run).add_done_callback(worker.done_callback)

    def join(self):
        self._executor.shutdown()
