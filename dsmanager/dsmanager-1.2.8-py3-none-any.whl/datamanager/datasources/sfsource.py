"""@Author: Rayane AMROUCHE

SalesForce Sources Handling.
"""

import os

from typing import Any
from getpass import getpass

import simple_salesforce  # type: ignore # pylint: disable=import-error

import pandas as pd  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource

from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger


class SFSource(DataSource):
    """Inherited Data Source Class for sql sources."""

    schema_read = DataStorage(
        {
            "source_type": "salesforce",
            "username_env_name": "sf_username_environment_variable_name",
            "password_env_name": "sf_password_environment_variable_name",
            "token_env_name": "sf_token_environment_variable_name",
            "domain_env_name": "sf_domain_environment_variable_name",
            "table_name": "TABLE",
            "args": {"simple_salesforce_argument_keyword": "value_for_this_argument"},
        }
    )

    @staticmethod
    @Logger.log_source("read", [])
    def read_source(
        username_env_name: str = "SF_USERNAME",
        password_env_name: str = "SF_PASSWORD",
        token_env_name: str = "SF_TOKEN",
        domain_env_name: str = "SF_DOMAIN",
        table_name: str = "",
        **kwargs: Any,
    ) -> Any:
        """Salesforce source reader.

        Args:
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.
            token_env_name (str): Name of the token env variable.
            domain_env_name (str): Name of the domain env variable.
            table_name (str): Name of the table in the dataset.

        Returns:
            Any: Data from source.
        """
        engine = simple_salesforce.Salesforce(
            username=os.getenv(username_env_name, None)
            or input(
                "Username environment name given is not found.\n"
                "Please enter direcly your salesforce username here:"
            ),
            password=os.getenv(password_env_name, None)
            or getpass(
                "Password environment name given is not found.\n"
                "Please enter direcly your salesforce password here:"
            ),
            security_token=os.getenv(token_env_name, None)
            or getpass(
                "Security token environment name given is not found.\n"
                "Please enter direcly your salesforce security token here:"
            ),
            domain=os.getenv(domain_env_name, None)
            or input(
                "Domain environment name given is not found.\n"
                "Please enter direcly your salesforce domain here:"
            ),
            **kwargs,
        )
        if table_name:
            column_list = (
                pd.DataFrame(getattr(engine, table_name).describe()["fields"])["name"]
            ).to_list()

            columns = ", ".join(column_list)
            query = f"""SELECT {columns} FROM {table_name}"""

            data = engine.query(query)["records"]
            data = pd.DataFrame.from_dict(data, orient="columns").drop(
                "attributes", axis=1
            )
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
        data = SFSource.read_source(
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            token_env_name=source_info["token_env_name"],
            domain_env_name=source_info["domain_env_name"],
            table_name=source_info["table_name"],
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
        engine = SFSource.read_source(
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            token_env_name=source_info["token_env_name"],
            domain_env_name=source_info["domain_env_name"],
            **source_info["args"],
        )
        return engine
