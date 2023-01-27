from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vectice.models.datasource.datawrapper.metadata import DatasetSourceUsage, FilesMetadata

_logger = logging.getLogger(__name__)


class DataWrapper(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name: str, usage: DatasetSourceUsage | None = None, inputs: list[int] | None = None):
        """Initialize a data wrapper.

        Parameters:
            usage: The usage of the dataset.
            name: The name of the [`DataWrapper`][vectice.models.datasource.datawrapper.data_wrapper.DataWrapper].
            inputs: The list of dataset ids to create a new dataset from.
        """
        self._old_name = name
        self._name = name
        self._inputs = inputs
        self._usage = usage
        self._metadata = None
        self._data = None

    @property
    def data(self) -> dict[str, bytes]:
        """The wrapper's data.

        Returns:
            The wrapper's data.
        """
        if self._data is None:
            self._data = self._fetch_data()  # type: ignore[assignment]
        return self._data  # type: ignore[return-value]

    @abstractmethod
    def _fetch_data(self) -> dict[str, bytes]:
        pass

    @abstractmethod
    def _build_metadata(self) -> FilesMetadata:
        pass

    @property
    def name(self) -> str:
        """The wrapper's name.

        Returns:
            The wrapper's name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set the wrapper's name.

        Parameters:
            value: The wrapper's name.
        """
        self._name = value
        self._clear_data_and_metadata()

    @property
    def usage(self) -> DatasetSourceUsage | None:
        """The wrapper's usage.

        Returns:
            The wrapper's usage.
        """
        return self._usage

    @property
    def inputs(self) -> list[int] | None:
        """The wrapper's inputs.

        Returns:
            The wrapper's inputs.
        """
        return self._inputs

    @property
    def metadata(self) -> FilesMetadata:
        """The wrapper's metadata.

        Returns:
            The wrapper's metadata.
        """
        if self._metadata is None:
            self.metadata = self._build_metadata()
        return self._metadata  # type: ignore[return-value]

    @metadata.setter
    def metadata(self, value):
        """Set the wrapper's metadata.

        Parameters:
            value: The metadata to set.
        """
        self._metadata = value

    def _clear_data_and_metadata(self):
        self._data = None
        self._metadata = None
