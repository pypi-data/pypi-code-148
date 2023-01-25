from __future__ import annotations
from typing import Callable


class Promulgation:
    """
    Promulgation.
    """

    listeners: dict[str, list[Callable[[Promulgation], None]]] = {}

    @classmethod
    def subscribe(cls, listener: Callable[[Promulgation], None]) -> None:
        """
        Register a function as handler for the given event.
        """
        if cls.__name__ not in cls.listeners:
            cls.listeners[cls.__name__] = []

        cls.listeners[cls.__name__].append(listener)

    @classmethod
    def unsubscribe(cls, listener: Callable[[Promulgation], None]) -> None:
        """
        Unregisters a handler for the given event.
        """
        if cls.__name__ not in cls.listeners:
            cls.listeners[cls.__name__] = []
        cls.listeners[cls.__name__].remove(listener)

    def promulgate(self) -> None:
        """
        Causes the registered handler to be called.
        """
        for listener in self.listeners.get(self.__class__.__name__, []):
            listener(self)
