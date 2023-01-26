from typing import List
import threading
import logging

from .LedDev import LedDev
from uun_iot_libledstrip import rgb2hex

logger_ds = logging.getLogger(__name__ + ".DebugLedDev")
try: 
    import colored
except ImportError:
    pass

class DebugLedDev(LedDev):
    """ Virtual debugging LED device.

    This can be used to debug applications without hardware LED devices at hand.

    Args:
        n: number of LEDs
        colored: attempt to use colored output in console (requires package `colored` to be installed), default to True. For Windows, import package `colorama` and run `colorama.init()` before working with this package.
    """

    _state: List[tuple]
    _n: int
    _colored: bool
    _lock: threading.Lock

    def __init__(self, n: int, colored: bool=True):
        logger_ds.info(f"Initialized a DebugLedDev with {n} pixels.")
        self._n = n
        self._state = [(0,0,0)] * n
        self._lock = threading.Lock()

        self._colored = colored
        if colored:
            try: 
                import colored
                self._colored = True
            except ImportError:
                logger_ds.debug("Falling back to text mode - package `colored` not found.")
                self._colored = False

    def __repr__(self):
        return str([rgb2hex(x) for x in self._state])

    def _colored_print(self):
        if self._colored:
            res = colored.attr('reset')
            print(" " + "---"*self._n + " ")
            print("|", end="")
            for x in self._state:
                color = colored.bg(rgb2hex(x))
                print(color + "  " + res, end=" ")
            print("|")
            print(" " + "---"*self._n + " ", flush=True)

    def show(self):
        with self._lock:
            if self._colored:
                self._colored_print()
            else:
                print(self)

    def __setitem__(self, index, val): 
        with self._lock:
            self._state[index] = val

    def __getitem__(self, index): 
        with self._lock:
            return self._state[index]

