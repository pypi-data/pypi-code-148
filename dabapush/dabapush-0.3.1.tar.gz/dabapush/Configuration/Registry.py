"""Registry for obtaining plug-ins."""
# pylint: disable=W0622
from importlib import import_module
from typing import Any, ChainMap, Dict, List, Optional, Type

import yaml
from loguru import logger as log

from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


class Registry(yaml.YAMLObject):
    """Handles plug-ins."""

    yaml_tag = "!dabapush:Registry"

    _instances = []

    """ """

    def __new__(cls):
        new_instance = super(Registry, cls).__new__(cls)
        Registry._instances.append(new_instance)

        return new_instance

    def __init__(
        self,
        readers: Optional[Dict[str, str]] = None,
        writers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__()

        self.readers = readers or {}
        self.writers = writers or {}

    def __del__(self):
        Registry._instances.remove(self)

    # --- static methods --- #

    @staticmethod
    def get_reader(type: str) -> Optional[Type[ReaderConfiguration]]:
        """Get a reader from the Registry.

        Parameters
        ----------
        type :
          str: registry key
        Returns:
          ReaderConfiguration or None: the requested ReaderConfiguration or None if
          no matching configuration is found.
        """
        _readers_: list[ReaderConfiguration] = [
            inst.readers for inst in Registry._instances
        ]
        readers = ChainMap(*_readers_)

        if type in readers:
            instance_info = readers[type]
            log.debug(
                f'Creating Configuration instance from {", ".join(instance_info)}.'
            )
            reader_configuration = getattr(
                import_module(instance_info["moduleName"], package="dabapush"),
                instance_info["className"],
            )

            return reader_configuration
        return None

    @staticmethod
    def get_writer(type: str) -> Optional[Type[WriterConfiguration]]:
        """Get a writer from the Registry.

        Parameters
        ----------
        type :
          str: registry key
        Returns:
          WriterConfiguration or None: the requested WriterConfiguration or None if
          no matching configuration is found.
        """
        _writers_ = [inst.writers for inst in Registry._instances]
        writers = ChainMap(*_writers_)

        if type in writers:
            instance_info = writers[type]
            log.debug(
                f'Creating Configuration instance from {", ".join(instance_info)}.'
            )
            writer_configuration = getattr(
                import_module(instance_info["moduleName"], package="dabapush"),
                instance_info["className"],
            )

            return writer_configuration
        return None

    @staticmethod
    def __ensure_reader__(arg: Any) -> bool:
        return issubclass(arg, ReaderConfiguration)

    @staticmethod
    def __ensure_writer__(arg: Any) -> bool:
        return issubclass(arg, WriterConfiguration)

    @staticmethod
    def list_all_readers() -> List[str]:
        """List all readers in Registries."""
        _readers_ = [inst.readers for inst in Registry._instances]
        readers = ChainMap(*_readers_)
        return [_ for _ in readers]

    @staticmethod
    def list_all_writers() -> List[str]:
        """List all writers in Registries."""
        _writers_ = [inst.writers for inst in Registry._instances]
        writers = ChainMap(*_writers_)
        return [_ for _ in writers]

    # --- instance methods --- #
    def register_reader(self, name: str, plugin_configuration) -> None:
        """Register a reader class.

        Parameters
        ----------
        name :
            str:

        plugin_configuration :
        """
        if Registry.__ensure_reader__(plugin_configuration):
            self.readers[name] = plugin_configuration

    def register_writer(self, name: str, constructor) -> None:
        """Register a writer class.

        Parameters
        ----------
        name :
            str: the identifying name
        constructor :
            Type[object]: the class to register
        """

    def remove_reader(self, name: str):
        """Remove a reader class from the registry.

        Parameters
        ----------
        name :
            str: identifier of the class to be removed

        Returns
        -------
        bool: True if class is found and removed, False otherwise.
        """

    def remove_writer(self, name: str):
        """

        Parameters
        ----------
        name :
            str:
        name :
            str:
        name :
            str:
        name: str :


        Returns
        -------

        """

    def list_writers(self) -> List[str]:
        """List writers."""

    def list_readers(self) -> List[str]:
        """List readers."""
