"""
Soil package.
"""
from soil import connectors, errors, finder
from soil.alerts import alerts
from soil.alias import alias
from soil.data import data
from soil.decorator import decorator
from soil.dictionary import dictionary
from soil.logger import logger

# pylint:disable=consider-using-from-import
from soil.modulify import modulify
from soil.task import task, task_wait

finder.upload_modules()

__all__ = [
    "modulify",
    "data_structures",
    "modules",
    "data",
    "alias",
    "logger",
    "connectors",
    "decorator",
    "task",
    "task_wait",
    "alerts",
    "dictionary",
    "errors",
]
