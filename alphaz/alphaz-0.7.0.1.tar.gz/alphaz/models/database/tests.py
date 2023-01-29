from sqlalchemy.orm import relationship

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
    Float,
    BLOB,
)

from .models import (
    AlphaTable,
    AlphaTableId,
    AlphaColumn,
    AlphaFloat,
    AlphaInteger,
    AlphaTableIdUpdateDate,
    AlphaTableUpdateDate,
    AlphaTablePrimaryIdUpdateDate,
)

from core import core, DB


class TestChild(DB.Model, AlphaTablePrimaryIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "test_child"

    name_ = AlphaColumn(String(30))
    text_ = AlphaColumn(String(300))
    number_ = AlphaColumn(Integer)
    date_ = AlphaColumn(DateTime)


class Test(DB.Model, AlphaTablePrimaryIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "test"

    name_ = AlphaColumn(String(30))
    text_ = AlphaColumn(String(300))
    number_ = AlphaColumn(Integer)
    date_ = AlphaColumn(DateTime)

    test_child_name = AlphaColumn(
        "test_child_id", Integer, ForeignKey("test_child.id"), nullable=True
    )
    test_child = relationship("TestChild")


class TestChilds(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "test_childs"

    id = AlphaColumn(Integer, autoincrement=True)

    parent_id = AlphaColumn(Integer, ForeignKey("test.id"), nullable=False,)
    child_parent_id = AlphaColumn(Integer, ForeignKey("test_child.id"), nullable=False,)

    name_ = AlphaColumn(String(30), primary_key=True)
    text_ = AlphaColumn(String(300))
    number_ = AlphaColumn(Integer)
    date_ = AlphaColumn(DateTime)

    parent = relationship("Test", backref="test_childs", cascade="all,delete")
