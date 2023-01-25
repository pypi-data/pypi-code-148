'''
# BAKit
Built-in Alternative Kit

'''

from .Events import Event, Events
from .Queue import Queue
from .tasks_queue import TasksQueue
from .Copy import copy
from .defer import defer
from .storage import Storage, Config, Environ

__version__ = "1.0.2"
__all__ = ["Event", "Events", "Queue", "tasks_queue", "copy", "defer", "TasksQueue",
           "Storage", "Config", "Environ"
           "storage", "config", "environ"]

storage = Storage()
config = Config()
environ = Environ()