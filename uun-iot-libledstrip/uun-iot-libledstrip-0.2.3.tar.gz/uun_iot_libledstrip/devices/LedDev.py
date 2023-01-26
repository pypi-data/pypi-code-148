from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class LedDev(ABC):
    """ Abstract class interface for the underlying hardware implementation of LED strip.

    Pixel colors are written in RGB tuple format directly into derived objects using list index syntax.
    Call :meth:`~LedDev.show` to propagate the written values.
    Some derived class accept parameter ``autoshow`` to control automatic `show-after-write` behaviour.

    Example:

        .. code-block:: python

            ledd = DebugLedDev(16)
            ledd[0] = (100, 200, 255)
            print(ledd[0])

        >>> (100,200,255)

    """
    _n: int

    @abstractmethod
    def __init__(self, *args, **kwargs): pass

    @abstractmethod
    def show(self): pass

    @abstractmethod
    def __setitem__(self, index, val): pass

    @abstractmethod
    def __getitem__(self, index): pass

    def __del__(self):
        for i in range(self._n):
            self[i] = (0,0,0)
        self.show()
        logger.debug(f"{self.__class__.__name__} cleared.")

