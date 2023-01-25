__all__ = ["Events"]

from threading import Thread
from threading import Event as _Event
from multiprocessing import Pool, Process
from time import sleep
from typing import Any
from signal import (
   signal,
   SIGINT   
)

class Event(_Event):
   def __init__(self, name:str, func=lambda:None) -> None:
      super().__init__()
      self._name = name
      self._func = func
      self._data = None

   @property
   def func(self):
      return self._func

   @property
   def data(self):
      return self._data
   
   @data.setter
   def data(self, value):
      self._data = value

   def clear(self) -> None:
      self.data = None
      return super().clear()

   def set(self) -> None:
      super().set()
      data = self.execute()
      self.clear()

      return data

   def execute(self):
      return self.func(self.data)

class Events:
   def __init__(self) -> None:
      self.events = {}

   def on(self, name:str):
      def decorator(func):
         self._add_event(name, func)
         return func
      
      return decorator
   
   def _add_event(self, name:str, func):
      if name in self.events:
         raise TypeError("event name already exist")
      
      if name in DefaultEvents.defaults:
         DefaultEvents.switch[name](func)

      self.events[name] = Event(name, func)

   def trigger(self, name:str, data:Any=None) -> Any:
      event = self.events.get(name)
      if not event:
         raise KeyError(f"no registered event with name '{name}'")
      
      event.data = data
      return event.set()

class DefaultEvents:
   def exit(func):
      def handler(signum, frame):
         func(None) # there is no data, so it's None
      
      signal(SIGINT, handler)

   defaults = ["exit"]
   switch = {
      "exit": exit
   }