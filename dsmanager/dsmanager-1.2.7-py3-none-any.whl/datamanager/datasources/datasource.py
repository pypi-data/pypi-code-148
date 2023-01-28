"""@Author: Rayane AMROUCHE

Data Sources Handling.
"""

import io

from typing import Any

import pandas as pd  # type: ignore

from dsmanager.datamanager.datastorage import DataStorage


class DataSource:
    """Data Source Class."""

    _file_schema = DataStorage(
        {
            "file_type": "csv | excel | text | json | ...",
            "encoding": "utf-8",
            "args": {"pandas_read_file_argument_keyword": "value_for_this_argument"},
        }
    )

    schema_read = {"params": "Read is not handled for this data source."}
    schema_write = {"params": "Write is not handled for this data source."}

    @staticmethod
    def _decode_files(
        file: Any, file_type: str = "csv", encoding: str = "utf-8", **kwargs: Any
    ) -> Any:
        data = None
        if file_type == "csv":
            data = pd.read_csv(file, **kwargs)
        elif file_type == "excel":
            data = pd.read_excel(file, **kwargs)
        elif file_type == "json":
            data = pd.Series(file)
        elif file_type == "text":
            with open(file, "r", encoding=encoding) as file_obj:
                data = file_obj.read()
        else:
            raise Exception("File type unknown or not supported.")
        return data

    @staticmethod
    def _encode_files(
        data: Any, file_type: str = "csv", encoding: str = "utf-8", **kwargs: Any
    ) -> Any:
        buffer = io.StringIO()
        if file_type == "csv":
            data.to_csv(buffer, **kwargs)
        elif file_type == "excel":
            data.to_excel(buffer, **kwargs)
        elif file_type == "json":
            data.to_json(buffer, **kwargs)
        else:
            raise Exception("File type unknown or not supported.")
        text = buffer.getvalue()
        return io.BytesIO(str.encode(text, encoding=encoding)).getvalue()

    @staticmethod
    def _load_source(source_info: dict, **kwargs: Any) -> None:
        source_info.update(**kwargs)
        if "args" not in source_info:
            source_info["args"] = {}

    @staticmethod
    def read(source_info: dict, **kwargs: Any) -> None:
        """Read source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            NotImplementedError: Raised if missing needed metadatas.
        """
        DataSource._load_source(source_info, **kwargs)
        raise NotImplementedError("This source does not handle read.")

    @staticmethod
    def write(
        source_info: dict,
        data: Any,  # pylint: disable=unused-argument
        **kwargs: Any,
    ) -> Any:
        """Write in a source and returns the response of the operation.

        Args:
            source_info (dict): Source metadatas.
            data (Any): Data to write in source.

        Raises:
            NotImplementedError: Raised if missing needed metadatas.
        """
        DataSource._load_source(source_info, **kwargs)
        raise NotImplementedError("This source does not handle write.")

    @staticmethod
    def read_db(source_info: dict, **kwargs: Any) -> None:
        """Read source and returns a source engine.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            NotImplementedError: Raised if missing needed metadatas.
        """
        DataSource._load_source(source_info, **kwargs)
        raise NotImplementedError("This source does not handle read_db.")

    @staticmethod
    async def async_read(source_info: dict, **kwargs: Any) -> None:
        """Asynchronously read source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            NotImplementedError: Raised if missing needed metadatas.
        """
        DataSource._load_source(source_info, **kwargs)
        raise NotImplementedError("This source does not handle async read.")

    @staticmethod
    async def async_read_db(source_info: dict, **kwargs: Any) -> None:
        """Asynchronously read source and returns a source engine.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            NotImplementedError: Raised if missing needed metadatas.
        """
        DataSource._load_source(source_info, **kwargs)
        raise NotImplementedError("This source does not handle async read_db.")
