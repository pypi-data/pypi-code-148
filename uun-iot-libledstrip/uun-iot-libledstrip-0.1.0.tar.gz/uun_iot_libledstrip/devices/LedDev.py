from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class LedDev(ABC):
    """ Abstract class interface for the underlying hardware implementation of LED strip. """
    _n: int

    @abstractmethod
    def __init__(self, pin, n, *args, **kwargs): pass

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

