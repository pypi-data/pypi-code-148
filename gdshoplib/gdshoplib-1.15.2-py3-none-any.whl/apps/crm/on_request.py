from typing import Optional

from pydantic import BaseModel, ValidationError

from gdshoplib.services.notion.models.props import PropModel


class OnRequestTable:
    def __init__(self, blocks, /, notion, parent):
        self.notion = notion
        self.parent = parent

        self._blocks = blocks
        self._rows = []

        self.__iter = None

    def _parse_rows(self):
        result = []
        for i, block in enumerate(self._blocks):
            row = []
            for r in block["table_row"]["cells"]:
                if not r:
                    row.append(None)
                    continue
                row.append(PropModel(page={}).get_type_data(r[0]))

            if row[4] == "Ошибка":
                continue

            row_result = dict(
                block_id=block["id"],
                name=row[0],
                link=row[1],
                price=row[2],
                quantity=row[3],
            )
            try:
                result.append(OnRequestTableRow(**row_result))
            except ValidationError as e:
                row_result["error"] = str(e)
                result.append(OnRequestTableInvalidRow(**row_result))
        return result

    @property
    def rows(self):
        if not self._rows:
            self._rows = self._parse_rows()
        return self._rows

    def __iter__(self):
        self.__iter = iter(self.rows)
        return self

    def __next__(self):
        return next(self.__iter)


class OnRequestTableRow(BaseModel):
    block_id: str
    name: str
    link: str
    price: float
    quantity: int
    error: Optional[str]


class OnRequestTableInvalidRow(BaseModel):
    block_id: str
    name: Optional[str]
    link: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    error: str
