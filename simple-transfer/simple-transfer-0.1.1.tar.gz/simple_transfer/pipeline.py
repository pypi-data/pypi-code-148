import logging
from typing import Literal, Optional

from simple_transfer import SIMPLE_TRANSFER_CONFIG, Connection, Extractor, Injector


class Pipeline:
    """
    Moves data from a source table/db into a destination table/db. Orchestrates the `Extractor` and `Injector`
    """

    def __init__(
        self,
        source_connection: Connection,
        source_schema: str,
        source_table: str,
        destination_connection: Connection,
        destination_schema: str,
        destination_table: str,
        intermediate_location: str = "",
        transport_params: Optional[dict] = None,
        inject_mode: Literal["overwrite", "append", "swap"] = "overwrite",
        where_clause: str = "",
    ):
        """
        Moves data from a source table/db into a destination table/db. Orchestrates the `Extractor` and `Injector`
        Parameters:
            source_connection (Connection) : The connection from which to extract the table.
            source_schema (str) : The schema from which to extract the table within the db.
            source_table (str) : The table from which to extract data from.

            destination_connection (Connection): The connection with which to insert the data.
            destination_schema (str) : The schema to inject the data within the destination db.
            destination_table (str) : The table to inject the extracted data into within the destination db.

            intermediate_location (str) : An intermediate directory to place the extracted data in. This can be a relative path, a absolute path, or a remote path (s3).
            transport_params (dict) : A dict which is passed through to `smart_open.open` `transport_params` argument. (Optional)
            inject_mode (str) : The injection mode (overwrite, append, swap).
            where_clause (str) : An optional where clause which will be used to filter the table extraction query. (Optional)
        """
        self.source_connection = source_connection
        self.source_schema = source_schema
        self.source_table = source_table
        self.where_clause = where_clause

        self.destination_connection = destination_connection
        self.destination_schema = destination_schema
        self.destination_table = destination_table

        self.intermediate_location = intermediate_location
        self.transport_params = transport_params

        self.inject_mode: Literal["overwrite", "append", "swap"] = inject_mode

    def execute(self):
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(
                "Executing pipeline from"
                f"\nsource ({self.source_connection} `{self.source_schema}`.`{self.source_table}`)"
                f"\nto destination ({self.destination_connection} `{self.destination_schema}`.`{self.destination_table}`)"
                f"\nusing intermediate location `{self.intermediate_location}`"
                f"\nand injection mode `{self.inject_mode}`"
            )
        with Extractor(
            self.source_connection,
            self.source_schema,
            self.source_table,
            self.intermediate_location,
            transport_params=self.transport_params,
            where_clause=self.where_clause,
        ) as e:
            e.extract()
            ddl_file = e.ddl_destination
            csv_file = e.csv_destination

        with Injector(
            self.destination_connection,
            self.destination_schema,
            self.destination_table,
            csv_file,
            ddl_file,
            transport_params=self.transport_params,
        ) as i:
            i.inject(self.inject_mode)
