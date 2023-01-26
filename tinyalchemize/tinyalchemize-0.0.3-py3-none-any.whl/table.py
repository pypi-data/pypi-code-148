from typing import Any, Dict, List, Sequence
from tinytable import Table
import tabulize
from tinytim.rows import row_dicts_to_data

from sqlalchemy.engine import Engine

from tinyalchemize.records import table_to_records, insert_record, insert_records

Record = Dict[str, Any]


class TinySqlTable(Table):
    def __init__(self, name: str, engine: Engine):
        self.sqltable = tabulize.SqlTable(name, engine)
        data = row_dicts_to_data(self.sqltable.old_records)
        super().__init__(data)

    @property
    def primary_keys(self) -> List[str]:
        return self.sqltable.primary_keys

    @primary_keys.setter
    def primary_keys(self, column_names: Sequence[str]) -> None:
        self.sqltable.primary_keys = list(column_names)

    def record_changes(self) -> Dict[str, List[Record]]:
        return self.sqltable.record_changes(self.records)

    @property
    def records(self) -> List[Record]:
       return table_to_records(self)

    def insert_record(self, record: Record) -> None:
        insert_record(self, record)

    def insert_records(self, records: Sequence[Record]) -> None:
        insert_records(self, records)

    def pull(self):
        self.sqltable.pull()

    def push(self) -> None:
        self.sqltable.push(self.records)
        self.pull()


    