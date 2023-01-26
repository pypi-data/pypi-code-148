from typing import Any, Dict, Generator, Iterable, List
from tinytable import Table
from tinytim.insert import insert_rows


Record = Dict[str, Any]


def table_to_records(table: Table) -> List[Record]:
    return [dict(row) for _, row in table.iterrows()]


def insert_record(table: Table, record: Record) -> None:
    table.data = insert_rows(table.data, [record])


def insert_records(table: Table, records: Iterable[Record]) -> None:
    table.data = insert_rows(table.data, records)


def iterrecords(df) -> Generator[dict, None, None]:
    for i, (_, series) in enumerate(df.iterrows()):
        yield series.to_dict()