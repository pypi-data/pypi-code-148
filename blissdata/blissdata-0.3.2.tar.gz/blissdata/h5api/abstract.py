"""Definition of the h5py-like Bliss Data API"""

from collections import abc
from abc import abstractmethod, abstractproperty
from typing import Iterator, Optional, Tuple
from numpy.typing import DTypeLike
from .utils import types


class Attributes(abc.Mapping):
    """Node attributes."""


class Node:
    """Node in the data tree."""

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def short_name(self) -> str:
        pass

    @abstractproperty
    def attrs(self) -> Attributes:
        pass

    @abstractproperty
    def parent(self) -> "Group":
        pass

    @abstractproperty
    def file(self) -> "File":
        pass


class Group(Node, abc.Mapping):
    """Node in the data tree which contains other nodes."""

    @abstractmethod
    def __getitem__(self, key: str) -> Node:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Node]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass


class Dataset(Node, abc.Sequence):
    """Node in the data tree which contains data."""

    @abstractmethod
    def __getitem__(self, idx: types.DataIndexType) -> types.DataType:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractproperty
    def dtype(self) -> DTypeLike:
        pass

    @abstractproperty
    def shape(self) -> Tuple[int]:
        pass

    @abstractproperty
    def size(self) -> int:
        pass

    @abstractproperty
    def ndim(self) -> int:
        pass


class File(Group):
    """Root node in the data tree."""

    def __enter__(self) -> "File":
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> Optional[bool]:
        self.close()

    @abstractmethod
    def close(self) -> None:
        pass

    @property
    def parent(self) -> None:
        return None
