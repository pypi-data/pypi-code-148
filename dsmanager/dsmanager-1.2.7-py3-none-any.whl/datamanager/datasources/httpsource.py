"""@Author: Rayane AMROUCHE

Http Sources Handling.
"""

import json

from typing import Any, Optional

import requests  # type: ignore
import aiohttp  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource

from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger

REQUEST_PARAMS = [
    "url",
    "data",
    "json",
    "params",
    "headers",
    "cookies",
    "files",
    "auth",
    "timeout",
    "allow_redirects",
    "proxies",
    "hooks",
    "stream",
    "verify",
    "cert",
    "data_type",
    "request_type",
]


class HttpSource(DataSource):
    """Inherited Data Source Class for http sources."""

    schema_read = DataStorage(
        {
            "source_type": "http",
            "request_type": "get",
            "data_type": "json | text | ...",
            "url": "http_uri",
            "args": {"requests_get|post_argument_keyword": "value_for_this_argument"},
        }
    )

    @staticmethod
    @Logger.log_source("read", ["request_type", "url"])
    def read_source(
        url: str = "",
        request_type: str = "get",
        data_type: str = "text",
        session: Optional[requests.Session] = None,
        close_session: bool = True,
        **kwargs: Any
    ) -> Any:
        """Http source reader.

        Args:
            url (str): Type of request. Defaults to "get".
            request_type (str, optional): Type of request. Defaults to "get".
            data_type (str, optional): Type of data output. Defaults to "text".
            session (requests.Session, optional): Http session. Defaults to None.
            close_session (bool, optional): If true the session will be closed after the
                request. Defaults to True.

        Raises:
            Exception: Raised if the type of request is not handled.

        Returns:
            Any: Data from source.
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    " AppleWebKit/537.36 (KHTML, like Gecko)"
                    " Chrome/96.0.4664.93 Safari/537.36"
                )
            }
        if session is None:
            session = requests.Session()
        if request_type == "get":
            data = session.get(url, **kwargs)
        elif request_type == "post":
            data = session.post(url, **kwargs)
        else:
            raise Exception("Request type not handled")
        if close_session:
            session.close()

        if data_type == "json":
            data = data.json()
        elif data_type == "text":
            data = data.text
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

        args = {}
        for param in REQUEST_PARAMS:
            if param in source_info:
                args[param] = source_info[param]
            if "args" in source_info and param in source_info["args"]:
                if param in args and isinstance(source_info[param], dict):
                    args[param].update(source_info["args"][param])
                else:
                    args[param] = source_info["args"][param]
                del source_info["args"][param]
        data = HttpSource.read_source(**args)
        return data

    @staticmethod
    async def async_read_source(
        url: str, request_type: str = "get", data_type: str = "text", **kwargs: Any
    ) -> Any:
        """Async http source reader.

        Args:
            url (str): Type of request. Defaults to "get".
            request_type (str, optional): Type of request. Defaults to "get".
            data_type (str, optional): Type of data output. Defaults to "text".
            close_session (bool, optional): If true the session will be closed after the
                request. Defaults to True.

        Raises:
            Exception: Raised if the type of request is not handled.

        Returns:
            Any: Data from source.
        """
        async with aiohttp.ClientSession() as session:
            if request_type == "get":
                async with session.get(url, **kwargs) as response:
                    data = await response.text()
            elif request_type == "post":
                async with session.post(url, **kwargs) as response:
                    data = await response.text()
            else:
                raise Exception("Request type not handled")

        if data_type == "json":
            data = json.loads(data)
        return data

    @staticmethod
    async def async_read(source_info: dict, **kwargs: Any) -> Any:
        """Asynchronously handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        args = {}
        for param in REQUEST_PARAMS:
            if param in source_info:
                args[param] = source_info[param]
            if "args" in source_info and param in source_info["args"]:
                if param in args and isinstance(source_info[param], dict):
                    args[param].update(source_info["args"][param])
                else:
                    args[param] = source_info["args"][param]
                del source_info["args"][param]
        data = await HttpSource.async_read_source(**args)
        return data
