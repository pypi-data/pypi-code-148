import RPi.GPIO as GPIO

import threading
import logging
from typing import List

from uun_iot_libledstrip import rgb2hex
from .LedDev import LedDev

logger_ds = logging.getLogger(__name__ + ".DebugLedDev")

class GPIODev(LedDev):
    """ 
    Create a pin-based light strip. Each pin controls exactly one light pixel.
    """

    _state: List[tuple]
    _n: int
    _colored: bool
    _lock: threading.Lock

    def __init__(self, pins: List[int], n=None, pin_numbering=None):
        """ Choose `pins`-numbering GPIO mode beforehand. """
        self._n = n if n is not None else len(pins)
        logger_ds.info(f"Initialized a PinDev on pins `{pins}` with {self._n} pixels.")
        self._pins = pins
        self._state = [(0,0,0)] * self._n
        self._lock = threading.Lock()

        if pin_numbering == "BCM":
            GPIO.setmode(GPIO.BCM)
        elif pin_numbering == "BOARD":
            GPIO.setmode(GPIO.BOARD)

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def __repr__(self):
        return str([rgb2hex(x) for x in self._state])

    def show(self):
        with self._lock:
            for led in range(self._n):
                pin = self._pins[led]
                if self._state[led] == (0,0,0):
                    GPIO.output(pin, GPIO.LOW)
                else:
                    GPIO.output(pin, GPIO.HIGH)

    def __setitem__(self, index, val): 
        with self._lock:
            self._state[index] = val

    def __getitem__(self, index): 
        with self._lock:
            return self._state[index]

    def __del__(self):
        self._state = [(0,0,0)] * self._n
        self.show()
        GPIO.cleanup()


