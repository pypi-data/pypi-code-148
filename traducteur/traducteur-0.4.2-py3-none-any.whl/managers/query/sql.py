from typing import Sequence, Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ..filters.base import BaseFilter
from ..filters.types import StringFilter, DatetimeFilter, NumberFilter, ExistsFilter
from ..filters.types.base import BaseTypeFilter


class QueryBuilderException(Exception):
    pass


class SQLQueryBuilder:
    def __init__(self, session: Session, cls):
        self.session = session
        self.cls = cls

        self.query = self.session.query(self.cls)

    def _add_string(self, str_filter: StringFilter, col: Column):
        if str_filter.exact:
            self.query = self.query.filter(col == str_filter.exact)
            return  # no more need for other filters

        if str_filter.includes:
            self.query = self.query.filter(col.like(f"%{str_filter.includes}%"))

        if str_filter.begin:
            self.query = self.query.filter(col.like(f"{str_filter.begin}%"))

        if str_filter.end:
            self.query = self.query.filter(col.like(f"%{str_filter.end}"))

    def _add_datetime(self, date_filter: DatetimeFilter, col: Column):
        if date_filter.start:
            self.query = self.query.filter(col > date_filter.start)

        if date_filter.end:
            self.query = self.query.filter(col < date_filter.end)

    def _add_number(self, number_filter: NumberFilter, col: Column):
        if number_filter.equal:
            self.query = self.query.filter(col == number_filter.equal)
            return  # no more need for other filters

        if number_filter.gt:
            self.query = self.query.filter(col > number_filter.gt)

        if number_filter.lt:
            self.query = self.query.filter(col < number_filter.lt)

    def _add_exists(self, exists_filter: ExistsFilter, col: Column):
        pass

    def add(self, filter_cls: BaseTypeFilter, col: str):
        try:
            prop: Column = getattr(self.cls, col)
            if not isinstance(prop, InstrumentedAttribute):
                raise Exception()
        except Exception:
            raise QueryBuilderException(f"{self.cls} has no column {col}!")

        if isinstance(filter_cls, StringFilter):
            self._add_string(filter_cls, prop)
        elif isinstance(filter_cls, DatetimeFilter):
            self._add_datetime(filter_cls, prop)
        elif isinstance(filter_cls, NumberFilter):
            self._add_number(filter_cls, prop)
        elif isinstance(filter_cls, ExistsFilter):
            self._add_exists(filter_cls, prop)
        else:
            raise QueryBuilderException(f"Invalid filter provided: {type(filter_cls)}!")

        return self

    def add_multiple(self, filters: Sequence[BaseTypeFilter], columns: Sequence[str]):
        if len(filters) != len(columns):
            raise QueryBuilderException(f"Inconsistent lengths between filters and columns: {len(filters)} != {len(columns)}!")

        for f, c in zip(filters, columns):
            self.add(f, c)

        return self

    def build(self, **kwargs):
        if 'filter' in kwargs:
            f: BaseFilter = kwargs.get('filter')
            if f is None:
                raise QueryBuilderException(f"Query filter is set but is None!")

            for col, type_filter in f.for_query().items():
                if type_filter is None:
                    continue
                self.add(type_filter, col)

        return self

    def all(self) -> Sequence[Sequence[Any]]:
        return self.query.all()

    def paginate(self, page: int, per_page: int = 30) -> Sequence[Sequence[Any]]:
        return self.query.limit(per_page).offset((page - 1) * per_page).all()

    def first(self) -> Optional[Sequence[Any]]:
        return self.query.first()
