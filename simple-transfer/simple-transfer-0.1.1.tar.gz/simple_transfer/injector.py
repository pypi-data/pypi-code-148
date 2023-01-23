import json
import logging
import os
from typing import Literal, Optional, TextIO, Union
from uuid import uuid4

import smart_open
from simple_transfer.config import SIMPLE_TRANSFER_CONFIG
from simple_transfer.connection import Column, Connection


class Injector:
    """
    Injects extracted data into a destination database table.
    Should be called using a `with` statement:
    ```
    with Injector(...) as i:
        i.inject('overwrite')
    ```
    """

    ddl_file: TextIO
    csv_file: TextIO

    def __init__(
        self,
        connection: Connection,
        schema: str,
        table: str,
        source_csv_location: str,
        source_ddl_location: str,
        transport_params: Optional[dict] = None,
    ):
        """
        Parameters:
            connection (Connection):  The connection with which to inject the table.
            schema (str) : The schema to inject the data within the db.
            table (str) : The table to inject the extract data into.
            source_csv_location (str): The path to the CSV file which will be loaded into the db. This can be a relative path, a absolute path, or a remote path (s3).
            source_ddl_location (str): The path to the DDL JSON file which will define the table in the db. This can be a relative path, a absolute path, or a remote path (s3).
            transport_params (dict) : A dict which is passed through to `smart_open.open` `transport_params` argument. (Optional)
        """
        self.connection = connection
        self.schema = schema
        self.table = table
        self.source_csv_location = source_csv_location
        self.source_ddl_location = source_ddl_location
        self.transport_params = transport_params

    def __enter__(self):
        self.connection.connect()
        self.csv_file = smart_open.open(
            self.source_csv_location, "r", transport_params=self.transport_params
        )
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Opened file `{self.source_csv_location}`")
        self.ddl_file = smart_open.open(
            self.source_ddl_location, "r", transport_params=self.transport_params
        )
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Opened file `{self.source_ddl_location}`")
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()
        self.csv_file.close()
        self.ddl_file.close()
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Closed file `{self.source_csv_location}`")
            logging.info(f"Closed file `{self.source_ddl_location}`")

    def inject(self, mode: Literal["overwrite", "append", "swap"] = "overwrite"):
        """
        Executes the injection into the database.
        Modes:
         - overwrite: This mode will drop and recreate the table if it exists before inserting the data into it.
         - append: This mode will create the table if it doesn't exist, and then insert the data into it.
         - swap: This mode will create a swap table and insert the data into it. Then in a transaction it will swap the names of the swap table and existing table.
        """
        columns = [Column(**c) for c in json.loads(self.ddl_file.read())]
        if mode == "swap":
            swap_id = uuid4().hex[:12]
            swap_table = f"{self.table}__{swap_id}"
            old_table = f"{self.table}__old"
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info(
                    f"Creating and inserting data into swap table `{self.schema}`.`{swap_table}`"
                )

            self.connection.execute(
                self.connection.generate_create_table_statement(
                    self.schema, swap_table, columns
                )
            )
            self.connection.import_csv(self.schema, swap_table, self.csv_file)
            self.connection.execute(
                self.connection.generate_create_table_statement(
                    self.schema,
                    self.table,
                    columns,
                )
            )
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info(
                    f"Performing swap from `{self.schema}`.`{swap_table}` to `{self.schema}`.`{self.table}`"
                )
            self.connection.execute_many(
                [
                    self.connection.generate_rename_table_statement(
                        self.schema, self.table, old_table
                    ),
                    self.connection.generate_rename_table_statement(
                        self.schema, swap_table, self.table
                    ),
                    self.connection.generate_drop_table_statement(
                        self.schema, old_table
                    ),
                ],
                [[], [], []],
            )
            return
        if mode == "overwrite":
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info(f"Dropping table `{self.schema}`.`{self.table}`")
            self.connection.execute(
                self.connection.generate_drop_table_statement(self.schema, self.table)
            )
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(
                f"Creating and inserting data into table `{self.schema}`.`{self.table}`"
            )
        self.connection.execute(
            self.connection.generate_create_table_statement(
                self.schema, self.table, columns
            )
        )
        self.connection.import_csv(self.schema, self.table, self.csv_file)
