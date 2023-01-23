import abc
from typing import Generator, Iterable, Optional, Sequence, TextIO, Tuple

from simple_transfer.column import Column
from simple_transfer.config import SIMPLE_TRANSFER_CONFIG


class NotConnectedException(Exception):
    pass


class Connection(abc.ABC):
    """
    The interface with which the simple-transfer package interacts with a database.
    To add support for a new SQL dialect simply implement this class spec.
    """

    @abc.abstractmethod
    def connect(self):
        """
        Open a connection to the database.
        """
        pass

    @abc.abstractmethod
    def close(self):
        """
        Close the connection to the database if it is open.
        """
        pass

    @abc.abstractmethod
    def select(
        self,
        query: str,
        args: Optional[Sequence] = None,
        batch_size: int = SIMPLE_TRANSFER_CONFIG.BATCH_SIZE,
    ) -> Generator[Tuple, None, None]:
        """
        Execute a select query on the database, return the rows as a Generator of Tuples
        """
        pass

    @abc.abstractmethod
    def execute(self, query: str, args: Optional[Sequence] = None):
        """
        Execute a query on the database, return nothing.
        """
        pass

    @abc.abstractmethod
    def execute_many(self, queries: Iterable[str], args: Iterable[Sequence] = []):
        """
        Execute many queries on the database within a transaction.
        """
        pass

    @abc.abstractmethod
    def extract_table_ddl(self, schema: str, table: str) -> Iterable[Column]:
        """
        Runs a query against the database extracting the table definition information from the information_schema
        """
        pass

    @abc.abstractmethod
    def extract_table(
        self, schema: str, table: str, where_clause: str = ""
    ) -> Generator[Tuple, None, None]:
        """
        Runs a select query against a given table in the database returning a Generator of Tuples of the data.
        Add an optional `where_clause` to filter the data which gets exported:
        ex: `YEAR(timestamp) = YEAR(CURRENT_DATE)`
        """
        pass

    @abc.abstractmethod
    def import_csv(self, schema: str, table: str, f: TextIO):
        """
        Imports the contents of a CSV file into a table on the database.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def generate_create_table_statement(
        schema: str, table: str, columns: Iterable[Column]
    ) -> str:
        """
        Generates a create table statement for the given table definition.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def generate_drop_table_statement(schema: str, table: str) -> str:
        """
        Generates a drop table statement for the given table.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def generate_rename_table_statement(schema: str, table: str, new_table: str) -> str:
        """
        Generates a rename table statement from `{schema}.{table}` to `{schema}.{new_table}`
        """
        pass
