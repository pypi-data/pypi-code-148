"""@Author: Rayane AMROUCHE

File Sources Handling.
"""

import io
import os

from typing import Any

import aiohttp  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.utils._func import find_type
from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger


class FileSource(DataSource):
    """Inherited Data Source Class for file sources."""

    schema_read = DataStorage(
        {
            "source_type": "file",
            "path": "local_path | online_uri",
            **DataSource._file_schema,
        }
    )

    @staticmethod
    @Logger.log_source("read", ["path"])
    def read_source(
        path: str = "input.csv",
        **kwargs: Any,
    ) -> Any:
        """File source reader.

        Args:
            path (str): Path or Uri of the datasource.

        Returns:
            Any: Data from source.
        """
        if "file_type" not in kwargs:
            kwargs["file_type"] = find_type(path)

        data = super(FileSource, FileSource)._decode_files(path, **kwargs)
        return data

    @staticmethod
    @Logger.log_source("write", ["path"])
    def write_source(
        data: Any = None,
        path: str = "output.csv",
        **kwargs: Any,
    ) -> Any:
        """File source reader.

        Args:
            path (str): Path or Uri of the datasource.

        Returns:
            Any: Data from source.
        """
        if "file_type" not in kwargs:
            kwargs["file_type"] = find_type(path)

        data = super(FileSource, FileSource)._encode_files(data, **kwargs)
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, "wb") as outfile:
            outfile.write(data)
        return data

    @staticmethod
    def read(source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        DataSource._load_source(source_info, **kwargs)
        data = FileSource.read_source(
            path=source_info["path"],
            **source_info["args"],
        )
        return data

    @staticmethod
    async def async_read_source(path: str, **kwargs: Any) -> Any:
        """Async file source reader.

        Args:
            path (str): Path or Uri of the datasource.

        Returns:
            Any: Data from source.
        """
        file_byte = None
        if "file_type" not in kwargs:
            kwargs["file_type"] = find_type(path)
        if path.startswith("http:") or path.startswith("https:"):
            async with aiohttp.ClientSession() as session:
                async with session.get(path) as response:
                    with io.StringIO(await response.text()) as text_io:
                        file_byte = io.StringIO(text_io.read())
        data = super(FileSource, FileSource)._decode_files(
            file_byte if file_byte else path, **kwargs
        )
        return data

    @staticmethod
    async def async_read(source_info: dict, **kwargs: Any) -> Any:
        """Asynchronously handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        DataSource._load_source(source_info, **kwargs)
        data = FileSource.async_read_source(
            path=source_info["path"],
            **source_info["args"],
        )
        return data

    @staticmethod
    def write(source_info: dict, data: Any, **kwargs: Any) -> Any:
        """Write in a source and returns the response of the operation.

        Args:
            source_info (dict): Source metadatas.
            data (Any): Data to write in source.

        Returns:
            Any: Number of lines added to the table.
        """
        DataSource._load_source(source_info, **kwargs)
        res = FileSource.write_source(
            data=data,
            path=source_info["path"],
            **source_info["args"],
        )
        return res
