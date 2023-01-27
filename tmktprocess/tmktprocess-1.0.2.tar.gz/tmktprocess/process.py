from threading import Thread, Event
from typing import Dict, Any, Optional, List, Callable


class Process(Thread):

    def __init__(self, func: Callable, event_callback: Optional[Event] = None):
        self._result: Optional[Any] = None
        self.event: Optional[Event] = event_callback
        self._func = func
        Thread.__init__(self, target=self._run)
        self._args: List[Any] = []
        self._kwargs: Dict[str, Any] = {}

    def start(self, *args, **kwargs):
        """
        Start the thread with calling the original Thread.start().

        ALL PARAMETERS WILL TRANSFER TO THE .EXEC() FUNCTION.
        :return: str, uuid
        """
        self._args = args
        self._kwargs = kwargs
        Thread.start(self)

    def _run(self, *args, **kwargs) -> None:
        """
        Execute your .exec() method and save the returned value for add the possibility to recover it with .join().
        """
        self._result = self._func(*args, **kwargs)
        if self.event:
            self.event.set()

    def join(self, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Wait the end of this thread and return the returned value of your .exec() implementation.
        :param timeout: Time to wait in seconds, default is None == forever.
        :return: the .exec() result if it's finish
        """
        Thread.join(self, timeout)
        return self._result
