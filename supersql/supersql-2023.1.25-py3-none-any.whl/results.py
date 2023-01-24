from typing import List, Union
from asyncpg import Record


class Row():
    def __init__(self, current):
        self._current = current

    def __getattr__(self, k: str):
        return self._data.get(k)

    def column(self, k: Union[str, int]):
        return self._current[k]


class Rows():
    def __init__(self, rows: list):
        self._data = rows
        self._rows = [Row(row) for row in rows]
    
    def __bool__(self):
        return bool(self._data)

    def row(self, n: int):
        n = n - 1
        if n < 0: raise IndexError('Only positive row counts please...')
        return self._rows[n - 1]

    @property
    def rows(self) -> List[Row]:
        return self._data


# row = rows.row(5) -> Row
# rows = rows.rows[:3] -> List[Row]
# row.first_name -> str
