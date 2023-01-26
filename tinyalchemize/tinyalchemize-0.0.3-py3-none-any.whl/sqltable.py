from typing import Any, Dict, Tuple
import tabulize as tz
import tinytable as tt
from tinytim.rows import row_dicts_to_data

from tinyalchemize.records import table_to_records

Record = Dict[str, Any]


class SqlTable:
    def __init__(self, name: str, engine) -> None:
        self.name = name
        self.engine = engine
        self._sqltable = tz.SqlTable(name, engine)
        
    def __repr__(self) -> str:
        return repr(self._sqltable)
        
    def pull(self) -> tt.Table:
        self._sqltable.pull()
        data = row_dicts_to_data(self._sqltable.old_records)
        return tt.Table(data)
    
    def push(self, table: tt.Table) -> None:
        records = table_to_records(table)
        self._sqltable.push(records)
        
    def record_changes(self, table: tt.Table) -> dict:
        records = table_to_records(table)
        return self._sqltable.record_changes(records)

    
def read_sqltable(name: str, engine) -> SqlTable:
    return SqlTable(name, engine)


def read_sqltable_dataframe(name: str,engine) -> Tuple[SqlTable, tt.Table]:
    sqltable = SqlTable(name, engine)
    table = sqltable.pull()
    return sqltable, table


def to_sql(table: tt.Table, sqltable: SqlTable) -> None:
    sqltable.push(table)
