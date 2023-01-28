"""@Author: Rayane AMROUCHE

Sql Sources Handling.
"""

import os

from urllib.parse import quote
from getpass import getpass
from typing import Any

import pandas as pd  # type: ignore
import sqlalchemy  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource

from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger


class SqlSource(DataSource):
    """Inherited Data Source Class for sql sources."""

    schema_read = DataStorage(
        {
            "source_type": "sql",
            "username_env_name": "sql_username_environment_variable_name",
            "password_env_name": "sql_password_environment_variable_name",
            "address": "sql_host:port",
            "dialect": "postgresql | mysql | snowflake | ...",
            "database": "database_name",
            "query": "SELECT * from TABLE LIMIT 10",
            "table_name": "TABLE",
            "args": {"sql_alchemy_engine_argument_keyword": "value_for_this_argument"},
        }
    )

    schema_write = DataStorage(
        {
            "source_type": "sql",
            "username_env_name": "sql_username_environment_variable_name",
            "password_env_name": "sql_password_environment_variable_name",
            "address": "sql_host:port",
            "dialect": "postgresql | mysql | snowflake | ...",
            "database": "database_name",
            "table_name": "TABLE",
            "args": {"sql_alchemy_engine_argument_keyword": "value_for_this_argument"},
        }
    )

    @staticmethod
    @Logger.log_source("read", ["database", "address", "query", "table_name"])
    def read_source(  # pylint: disable=too-many-arguments
        dialect: str = "",
        username_env_name: str = "SQL_USERNAME",
        password_env_name: str = "SQL_PASSWORD",
        address: str = "",
        database: str = "",
        query: str = "",
        table_name: str = "",
        **kwargs: Any,
    ) -> Any:
        """Sql source reader.

        Args:
            dialect (str): Sqlalchemy dialect for the sql server.
            username_env_name (str): Username name in env to access the sql server.
            password_env_name (str): Password name in env to access the sql server.
            address (str): Address of the sql server.
            database (str): Database to access in the sql server.
            query (str, optional): Sql query. Defaults to "".
            table_name (str, optional): Table name to query. Defaults to "".

        Returns:
            Any: Data from source.
        """
        username = os.getenv(username_env_name, None) or input(
            "Username environment name given is not found.\n"
            "Please enter direcly your username here:"
        )
        password = os.getenv(password_env_name, None) or getpass(
            "Password environment name given is not found.\n"
            "Please enter direcly your password here:"
        )
        uri = f"{dialect}://{username}:{quote(password)}@{address}/{database}"
        engine = sqlalchemy.create_engine(uri)
        if query:
            conn = engine.connect()
            data = pd.read_sql_query(query, conn, **kwargs)
            conn.close()
        elif table_name:
            conn = engine.connect()
            data = pd.read_sql_table(table_name, conn, **kwargs)
            conn.close()
        else:
            data = engine

        return data

    @staticmethod
    @Logger.log_source("write", ["database", "address", "table_name"])
    def write_source(  # pylint: disable=too-many-arguments
        data: Any = None,
        dialect: str = "",
        username_env_name: str = "SQL_USERNAME",
        password_env_name: str = "SQL_PASSWORD",
        address: str = "",
        database: str = "",
        table_name: str = "",
        **kwargs: Any,
    ) -> int:
        """Sql source reader.

        Args:
            data (Any): Data to upload to the sql server.
            dialect (str): Sqlalchemy dialect for the sql server.
            username_env_name (str): Username name in env to access the sql server.
            password_env_name (str): Password name in env to access the sql server.
            address (str): Address of the sql server.
            database (str): Database to access in the sql server.
            table_name (str, optional): Table name to query. Defaults to "".

        Returns:
            int: Number of line pushed.
        """
        user = os.getenv(username_env_name, "")
        password = os.getenv(password_env_name, "")
        uri = f"{dialect}://{user}:{quote(password)}@{address}/{database}"
        engine = sqlalchemy.create_engine(uri)
        conn = engine.connect()
        res = 0
        if data:
            res = data.to_sql(
                table_name,
                con=conn,
                **kwargs,
            )
        conn.close()

        return res

    @staticmethod
    def read(source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        DataSource._load_source(source_info, **kwargs)

        data = SqlSource.read_source(
            dialect=source_info["dialect"],
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            address=source_info["address"],
            database=source_info["database"],
            query=source_info["query"] if "query" in source_info else "",
            table_name=source_info["table_name"] if "table_name" in source_info else "",
            **source_info["args"],
        )
        return data

    @staticmethod
    def read_db(source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns a source engine.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source engine.
        """
        DataSource._load_source(source_info, **kwargs)
        engine = SqlSource.read_source(
            dialect=source_info["dialect"],
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            address=source_info["address"],
            database=source_info["database"],
            **source_info["args"],
        )
        return engine

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
        res = SqlSource.write_source(
            data=data,
            dialect=source_info["dialect"],
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            address=source_info["address"],
            database=source_info["database"],
            table_name=source_info["table_name"],
            **source_info["args"],
        )
        return res
