from typing import List, TypeVar, Optional, Generic, Union, Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from .query import SQLQueryBuilder

T = TypeVar("T")


class SQLModelManager(Generic[T]):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    @property
    def engine(self):
        return create_engine(self.connection_string, echo=False, future=False)

    def session(self) -> Session:
        return Session(self.engine)

    def insert(self, item: T) -> T:
        with self.session() as session:
            session.add(item)
            session.commit()

            return self.get(type(item), item.id)

    def insert_many(self, items: List[T]):
        with self.session() as session:
            session.add_all(items)
            session.commit()

    def update(self, item: T) -> T:
        with self.session() as session:
            session.commit()

            return self.get(type(item), item.id)

    def delete(self, item: T) -> T:
        with self.session() as session:
            session.delete(item)
            session.commit()
            return item

    def get(self, cls, id: Union[str, int]) -> Optional[T]:
        with self.session() as session:
            return session.query(cls).get(id)

    def exists(self, cls, id: Union[str, int]) -> bool:
        with self.session() as session:
            return session.query(exists().where(cls.id == id)).scalar()

    def all(self, cls, **kwargs) -> List[T]:
        with self.session() as session:
            qb = SQLQueryBuilder(session, cls)
            return qb.build(**kwargs).all()

    def paginate(self, cls, page: int, per_page: int = 30, **kwargs) -> List[T]:
        with self.session() as session:
            qb = SQLQueryBuilder(session, cls).build(**kwargs)
            return qb.paginate(page, per_page)

    def query(self, query, one: bool = False, **kwargs) -> Union[Iterable[T], T]:
        with self.session() as session:
            return session.scalars(query).one() if one else session.scalars(query)


