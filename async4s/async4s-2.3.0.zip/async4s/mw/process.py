#!/usr/bin/env python

"""
Master-Worker模型-多进程实现方式
"""

from __future__ import annotations

import multiprocessing
import abc

__all__ = ["Master", "Worker"]


class Worker(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def done_callback(self, result):
        pass

    def error_callback(self, result):
        pass


class Master(object):
    def __init__(self, max_workers: int = None):
        self._executor = multiprocessing.Pool(processes=max_workers)

    def start(self, worker: Worker):
        self._executor.apply_async(func=worker.run, callback=worker.done_callback, error_callback=worker.error_callback)

    def join(self):
        self._executor.close()
        self._executor.join()
