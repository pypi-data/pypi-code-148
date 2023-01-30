from __future__ import annotations
from abc import ABC, abstractmethod

class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the conector objects.
    """

    @property
    @abstractmethod
    def conector(self) -> None:
        pass

    @abstractmethod
    def auth(self, token, api_key) -> None:
        pass

    @abstractmethod
    def configs(self, object='planos', **kwargs) -> None:
        pass

    # @abstractmethod
    # def fetch(self) -> None:
    #     pass