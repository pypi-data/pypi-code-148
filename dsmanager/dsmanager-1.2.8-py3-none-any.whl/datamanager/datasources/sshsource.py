"""@Author: Rayane AMROUCHE

Local Sources Handling.
"""

import os

from typing import Any
from getpass import getpass

import paramiko  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource

from dsmanager.datamanager.utils._func import find_type
from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger


class SshSource(DataSource):
    """Inherited Data Source Class for ssh sources."""

    schema_read = DataStorage(
        {
            "source_type": "ssh",
            "server": "ssh_server_address",
            "port": 21,
            "username_env_name": "ssh_username_environment_variable_name",
            "password_env_name": "ssh_password_environment_variable_name",
        }
    )

    @staticmethod
    @Logger.log_source("read", ["server", "port", "path"])
    def read_source(
        server: str = "",
        port: int = 22,
        username_env_name: str = "FTP_USERNAME",
        password_env_name: str = "FTP_PASSWORD",
        path: str = "",
        **kwargs: Any
    ) -> Any:
        """Ftp source reader.

        Args:
            server (str): Server address.
            port (int): Port of the server.
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.
            path (str, optional): Path of the file in the server.

        Returns:
            Any: Data from source.
        """
        username = os.getenv(username_env_name, None) or input(
            "Username environment name given is not found.\n"
            "Please enter direcly your ssh username here:"
        )
        password = os.getenv(password_env_name, None) or getpass(
            "Password environment name given is not found.\n"
            "Please enter direcly your ssh password here:"
        )

        try:
            transport = paramiko.Transport((server, port))
            transport.connect(None, username, password)
            engine = paramiko.SFTPClient.from_transport(transport)
        except paramiko.SSHException as _:
            engine = paramiko.SSHClient()
            engine.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            engine.connect(server, port=port, username=username, password=password)

        if path and isinstance(engine, paramiko.SFTPClient):
            file = engine.open(path)
            if "file_type" not in kwargs:
                kwargs["file_type"] = find_type(path)
            data = super(SshSource, SshSource)._decode_files(file, **kwargs)
            engine.close()
        else:
            data = engine
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
        data = SshSource.read_source(
            server=source_info["server"],
            port=source_info["port"],
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            path=source_info["path"],
            **source_info["args"],
        )
        return data

    @staticmethod
    def read_db(source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns an ssh source engine.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            Exception: Raised if missing needed metadatas.

        Returns:
            Any: Source engine.
        """
        DataSource._load_source(source_info, **kwargs)
        engine = SshSource.read_source(
            server=source_info["server"],
            port=source_info["port"],
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            **source_info["args"],
        )
        return engine
