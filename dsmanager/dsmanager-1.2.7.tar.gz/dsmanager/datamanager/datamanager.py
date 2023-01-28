"""@Author: Rayane AMROUCHE

Datamanager Class.
"""

import json
import logging
import asyncio
import inspect
import datetime

from typing import Any, Optional
from dotenv import load_dotenv  # type: ignore

import decorator  # type: ignore

from dsmanager.controller.config import Config
from dsmanager.controller.logger import Logger
from dsmanager.controller.utils import json_to_dict, format_dict
from dsmanager.controller._async import force_sync

from dsmanager.datamanager.utils import Utils
from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.datamanager.datasources.filesource import FileSource
from dsmanager.datamanager.datasources.httpsource import HttpSource
from dsmanager.datamanager.datasources.sqlsource import SqlSource
from dsmanager.datamanager.datasources.ftpsource import FtpSource
from dsmanager.datamanager.datasources.sshsource import SshSource

SOURCES = {
    "file": FileSource,
    "http": HttpSource,
    "sql": SqlSource,
    "ftp": FtpSource,
    "ssh": SshSource,
}

try:
    from dsmanager.datamanager.datasources.sharepointsource import SharepointSource

    SOURCES["sharepoint"] = SharepointSource
except ModuleNotFoundError as m_error:
    logging.getLogger(None).warning(
        "'SharepointSource' is not available because '%s' is missing.", m_error.name
    )
try:
    from dsmanager.datamanager.datasources.sfsource import SFSource

    SOURCES["salesforce"] = SFSource
except ModuleNotFoundError as m_error:
    logging.getLogger(None).warning(
        "'SFSource' is not available because '%s' is missing.", m_error.name
    )
try:
    from dsmanager.datamanager.datasources.kagglesource import KaggleSource

    SOURCES["kaggle"] = KaggleSource
except ModuleNotFoundError as m_error:
    logging.getLogger(None).warning(
        "'KaggleSource' is not available because '%s' is missing.", m_error.name
    )
except (OSError, ValueError) as o_error:
    logging.getLogger(None).warning(
        "'KaggleSource' is not available. More details: %s", o_error
    )


class DataManager:
    """DataManager class handle all the data work."""

    class _Datas(DataStorage):
        """A dictionary that can be accessed through attributes and called to get a
        dataset."""

        def __init__(self, __dm: Any) -> None:
            self.__dm = __dm
            self.__name__ = "datas"
            super().__init__()

        def __call__(  # pylint: disable=too-many-arguments
            self,
            name: str,
            save: bool = True,
            reload: bool = False,
            formatting: Optional[dict] = None,
            alias: str = "",
            **kwargs: Any,
        ):
            """Get info for a given source and return its data.

            Args:
                name (str): Name of the data source.
                save (bool, optional): If True save the data. Defaults to True.
                reload (bool, optional): If False try to load from datas. Defaults to
                    False.
                formatting (dict, optional): Source metadata formatting.
                alias (str, optional): Alias name for the source.

            Returns:
                Any: Requested data.
            """
            if not reload and name in self:
                data = self[name]
            else:
                source_info = self.__dm._get_source_info(name)
                if formatting is not None:
                    format_dict(source_info, formatting)
                source = self.__dm._get_source_reader(source_info)
                data = source.read(source_info, **kwargs)
            if save:
                self[name] = data
            if alias:
                self[alias] = data
            return data

    class _Sessions(DataStorage):
        """A dictionary that can be accessed through attributes and called to get a
        sessions."""

        def __init__(self, __dm: Any) -> None:
            self.__dm = __dm
            self.__name__ = "datas"
            super().__init__()

        def __call__(  # pylint: disable=too-many-arguments
            self,
            name: str,
            save: bool = True,
            reload: bool = False,
            formatting: Optional[dict] = None,
            alias: str = "",
            **kwargs: Any,
        ) -> Any:
            """Get info for a given source and return its data.

            Args:
                name (str): Name of the data source.
                save (bool, optional): If True save the session. Defaults to True.
                reload (bool, optional): If False try to load from sessions. Defaults to
                    False.
                formatting (dict, optional): Source metadata formatting.
                alias (str, optional): Alias name for the source.

            Returns:
                Any: Requested session engine.
            """
            if not reload and name in self:
                data = self[name]
            else:
                source_info = self.__dm._get_source_info(name)
                if formatting:
                    format_dict(source_info, formatting)
                source = self.__dm._get_source_reader(source_info)
                data = source.read_db(source_info, **kwargs)
            if save:
                self[name] = data
            if alias:
                self[alias] = data
            return data

    def __init__(
        self,
        metafile_path: str = "data/metadata.json",
    ) -> None:
        """Init Datamanager by giving the datasets metadata path.

        Args:
            metafile_path (str, optional): Path of the metadata file of the datasets.
                Defaults to "data/metadata.json".
        """
        load_dotenv(Config.get_option("env_path"))
        Logger.update_logger(name="datamanager")
        Logger.update_logger(name="datasource")

        if metafile_path:
            json_to_dict(metafile_path)

        self.sessions = self._Sessions(self)
        self.datas = self._Datas(self)
        self.__metadata_path = metafile_path
        self.datasources = DataStorage()
        self.utils = Utils(self)

        for source_name, source_module in SOURCES.items():
            self.add_datasource(source_name, source_module)

    def __repr__(self) -> str:
        res = "DataManager:\n"
        res += f"Metadata's path: {repr(self.__metadata_path)}\n"
        res += f"Metadata: {list(json_to_dict(self.__metadata_path).keys())}\n"
        res += f"Handled sources: {list(self.datasources.keys())}\n"
        res += f"Loaded datas: {list(self.datas.keys())}\n"
        res += f"Loaded sessions: {list(self.sessions.keys())}\n"
        return res

    @classmethod
    def preload(cls, metafile_path: str = "data/metadata.json") -> Any:
        """Init a DataManager and preload all sources.

        Args:
            metafile_path (str, optional): Path of the metadata file of the datasets.
                Defaults to "data/metadata.json".
        Returns:
            Datamanager: DataManager preloaded.
        """
        self = DataManager(metafile_path)
        metadata = json_to_dict(self.__metadata_path)
        for key in metadata.keys():
            try:
                self.get_data(key)
                Logger.get_logger("datamanager").info("Preloaded data %s.", key)
            except Exception as _:  # pylint: disable=broad-except
                try:
                    self.get_session(key)
                except Exception as dm_e:  # pylint: disable=broad-except
                    Logger.get_logger("datamanager").warning(
                        "Failed to preload '%s' with message : '%s'.", key, dm_e
                    )
        return self

    def add_datasource(self, name: str, source: Any) -> None:
        """Add a source class to datasources dict.

        Args:
            name (str): Name of the source.
            source (DataSource): Data Source class.
        """
        self.datasources[name] = source

        @decorator.decorator
        def decorate_read(__f, *args, **kwargs):
            signature = inspect.signature(__f).bind(*args, **kwargs)
            signature.apply_defaults()
            metadata = signature.arguments
            metadata["source_type"] = name
            metadata["args"] = metadata["kwargs"]
            del metadata["kwargs"]
            metadata_name = name + datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            self.add_source(metadata_name, metadata)
            return __f(*args, **kwargs)

        try:
            setattr(self, f"read_{name}", decorate_read(source.read_source))
        except AttributeError as _:
            ...

    def add_source(self, name: str, source_info: dict) -> None:
        """Add a source class to sources dict.

        Args:
            name (str): Name of the source.
            source (DataSource): Data Source class.
        """
        if self.__metadata_path:
            Logger.get_logger("datamanager").info(
                "Add source as '%s' to the DataManager metadatas", name
            )
        else:
            Logger.get_logger("datamanager").warning(
                "No metadata path provided. Cannot add '%s' to your sources.", name
            )
            return
        metadata = json_to_dict(self.__metadata_path)
        metadata[name] = source_info
        with open(self.__metadata_path, "w", encoding="utf-8") as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

    def get_sources(self) -> dict:
        """Getter for metadatas source.

        Returns:
            dict: Metadatas dict.
        """
        metadata = json_to_dict(self.__metadata_path)
        return metadata

    def _get_source_info(self, name: str) -> dict:
        """Handle access to metadata info for a given source.

        Args:
            name (str): Name of the source to access.

        Raises:
            KeyError: Raised if the name given is not in the metadata.

        Returns:
            dict: Return the metadata of the data source.
        """
        metadata = json_to_dict(self.__metadata_path)
        if name not in metadata:
            raise KeyError(f"{name} not in the metadata file.")
        data = metadata[name]
        return data

    def _get_source_reader(self, source_info: dict) -> Any:
        """Get data sources reader for a given data source's metadata.

        Args:
            source_info (dict): Metadata of a data source.

        Raises:
            NotImplementedError: Raised if the source is not handled.

        Returns:
            DataSource: Data source reader.
        """
        if "source_type" in source_info:
            source_type = source_info["source_type"]
            del source_info["source_type"]
        else:
            source_type = "file"

        if source_type in self.datasources:
            source_class = self.datasources[source_type]
        else:
            raise NotImplementedError(
                f"Data source '{source_type}' unknown or not supported"
            )

        return source_class

    def get_data(  # pylint: disable=too-many-arguments
        self,
        name: str,
        save: bool = True,
        reload: bool = False,
        formatting: Optional[dict] = None,
        alias: str = "",
        **kwargs: Any,
    ) -> Any:
        """Get info for a given source and return its data.

        Args:
            name (str): Name of the data source.
            save (bool, optional): If True save the data. Defaults to True.
            reload (bool, optional): If False try to load from datas. Defaults to False.
            formatting (dict, optional): Source metadata formatting.
            alias (str, optional): Alias name for the source.

        Returns:
            Any: Requested data.
        """
        if not reload and name in self.datas:
            data = self.datas[name]
        else:
            source_info = self._get_source_info(name)
            if formatting is not None:
                format_dict(source_info, formatting)
            source = self._get_source_reader(source_info)
            data = source.read(source_info, **kwargs)
        if save:
            self.datas[name] = data
        if alias:
            self.datas[alias] = data
        return data

    def get_session(  # pylint: disable=too-many-arguments
        self,
        name: str,
        save: bool = True,
        reload: bool = False,
        formatting: Optional[dict] = None,
        alias: str = "",
        **kwargs: Any,
    ) -> Any:
        """Get info for a given source and return its data.

        Args:
            name (str): Name of the data source.
            save (bool, optional): If True save the session. Defaults to True.
            reload (bool, optional): If False try to load from sessions. Defaults to
                False.
            formatting (dict, optional): Source metadata formatting.
            alias (str, optional): Alias name for the source.

        Returns:
            Any: Requested session engine.
        """
        if not reload and name in self.sessions:
            data = self.sessions[name]
        else:
            source_info = self._get_source_info(name)
            if formatting:
                format_dict(source_info, formatting)
            source = self._get_source_reader(source_info)
            data = source.read_db(source_info, **kwargs)
        if save:
            self.sessions[name] = data
        if alias:
            self.sessions[alias] = data
        return data

    def upload(  # pylint: disable=too-many-arguments
        self,
        name: str,
        data: Any,
        formatting: Optional[dict] = None,
        **kwargs: Any,
    ) -> Any:
        """Get info for a given source and upload data to it.

        Args:
            name (str): Name of the data source.
            data (Any, optional): Data to save.
            formatting (dict, optional): Source metadata formatting.

        Returns:
            Any: Result after pushing data.
        """
        source_info = self._get_source_info(name)
        if formatting is not None:
            format_dict(source_info, formatting)
        source = self._get_source_reader(source_info)
        res = source.write(source_info, data, **kwargs)
        return res

    async def pipe_get_data(  # pylint: disable=too-many-arguments
        self,
        name: str,
        save: bool = True,
        reload: bool = False,
        formatting: Optional[dict] = None,
        alias: str = "",
        **kwargs: Any,
    ) -> Any:
        """Get info for a given source and return its data asynchronously.

        Args:
            name (str): Name of the data source.
            save (bool, optional): If True save the data. Defaults to True.
            reload (bool, optional): If False try to load from datas. Defaults to False.
            formatting (dict, optional): Source metadata formatting.
            alias (str, optional): Alias name for the source.

        Returns:
            Any: Requested data.
        """

        if not reload and name in self.datas:
            data = self.datas[name]
        else:
            source_info = self._get_source_info(name)
            if formatting is not None:
                format_dict(source_info, formatting)
            source = self._get_source_reader(source_info)
            data = await source.async_read(source_info, **kwargs)
        if save:
            self.datas[name] = data
        if alias:
            self.datas[alias] = data

        return data

    @force_sync
    async def batch_load_async(self, async_calls: tuple) -> Any:
        """Launch a batch of asynchronous data loader.

        Args:
            async_calls (tuple): Asynchronous calls as a tuple of function, arguments
                and keyword arguments.

        Returns:
            Any: All the datas loaded in an array.
        """
        return await asyncio.gather(*async_calls)
