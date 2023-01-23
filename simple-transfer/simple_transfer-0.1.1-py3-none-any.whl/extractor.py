import csv
import json
import logging
import os
from typing import Optional, TextIO

import smart_open
from simple_transfer.config import SIMPLE_TRANSFER_CONFIG
from simple_transfer.connection import Connection


class Extractor:
    """
    Extracts a given table from a `Connection` to a `CSV` file and `DDL` json file.
    Should be called using a `with` statement:
    ```
    with Extractor(...) as e:
        e.extract()
    ```
    """

    csv_file: TextIO
    ddl_file: TextIO

    def __init__(
        self,
        connection: Connection,
        schema: str,
        table: str,
        destination: str,
        transport_params: Optional[dict] = None,
        where_clause: str = "",
    ):
        """
        Parameters:
            connection (Connection):  The connection from which to extract the table.
            schema (str) : The schema from which to extract the table within the db.
            table (str) : The table from which to extract data from.
            destination (str) : An intermediate directory to place the extracted data in. This can be a relative path, a absolute path, or a remote path (s3).
            transport_params (dict) : A dict which is passed through to `smart_open.open` `transport_params` argument. (Optional)
            where_clause (str) : An optional where clause which will be used to filter the table extraction query.
        """
        self.connection = connection
        self.schema = schema
        self.table = table
        self.where_clause = where_clause
        self.csv_destination = os.path.join(
            destination, f"{schema.lower()}__{table.lower()}.csv"
        )
        self.ddl_destination = os.path.join(
            destination, f"DDL_{schema.lower()}__{table.lower()}.json"
        )
        self.transport_params = transport_params

    def __enter__(self):
        self.connection.connect()
        self.csv_file = smart_open.open(
            self.csv_destination, "w", transport_params=self.transport_params
        )
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Opened file `{self.csv_destination}`")
        self.ddl_file = smart_open.open(
            self.ddl_destination, "w", transport_params=self.transport_params
        )
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Opened file `{self.ddl_destination}`")
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()
        self.csv_file.close()
        self.ddl_file.close()
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Closed file `{self.csv_destination}`")
            logging.info(f"Closed file `{self.ddl_destination}`")

    def extract(self):
        """
        Executes the extraction.
        """
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(
                f"Extracting columns from information schema for `{self.schema}`.`{self.table}`"
            )
        columns = self.connection.extract_table_ddl(self.schema, self.table)
        self.ddl_file.write(json.dumps([c.to_dict() for c in columns], default=str))
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(
                f"Extracting data from `{self.schema}`.`{self.table}` to `{self.csv_destination}`"
            )
        writer = csv.writer(self.csv_file, delimiter=",")
        rows_generator = self.connection.extract_table(
            self.schema, self.table, where_clause=self.where_clause
        )
        writer.writerow([c.name for c in columns])
        for row in rows_generator:
            writer.writerow(row)
