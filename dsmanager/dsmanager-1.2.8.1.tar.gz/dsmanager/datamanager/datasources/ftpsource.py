"""@Author: Rayane AMROUCHE

Ftp Sources Handling.
"""

import os
import urllib.request

from contextlib import closing
from typing import Any
from getpass import getpass

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.utils._func import find_type
from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger


class FtpSource(DataSource):
    """Inherited Data Source Class for ftp sources."""

    schema_read = DataStorage(
        {
            "source_type": "ftp",
            "username_env_name": "server_username_environment_variable_name",
            "password_env_name": "server_password_environment_variable_name",
            "server": "ftp_server_address",
            "port": 21,
            **DataSource._file_schema,
        }
    )

    @staticmethod
    @Logger.log_source("read", ["server", "port", "path"])
    def read_source(
        username_env_name: str = "FTP_USERNAME",
        password_env_name: str = "FTP_PASSWORD",
        server: str = "",
        port: int = 22,
        path: str = "",
        **kwargs: Any,
    ) -> Any:
        """Ftp source reader.

        Args:
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.
            server (str): Server address.
            port (int): Port of the server.
            path (str): Path of the file in the server.

        Returns:
            Any: Data from source.
        """
        username = os.getenv(username_env_name, None) or input(
            "Username environment name given is not found.\n"
            "Please enter direcly your ftp username here:"
        )
        password = os.getenv(password_env_name, None) or getpass(
            "Password environment name given is not found.\n"
            "Please enter direcly your ftp password here:"
        )
        if "file_type" not in kwargs:
            kwargs["file_type"] = find_type(path)
        path = f"ftp://{username}:{password}@{server}:{port}/{path}"
        with closing(urllib.request.urlopen(path)) as ftp_file:
            data = super(FtpSource, FtpSource)._decode_files(ftp_file, **kwargs)
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
        data = FtpSource.read_source(
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            server=source_info["server"],
            port=source_info["port"],
            path=source_info["path"],
            **source_info["args"],
        )
        return data
