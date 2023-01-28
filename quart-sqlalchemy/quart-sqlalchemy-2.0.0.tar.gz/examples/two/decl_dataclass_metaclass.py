from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Annotated
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import column_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import WriteOnlyMapped


metadata = MetaData()
reg = registry(metadata=metadata)

intpk = Annotated[int, mapped_column(init=False, primary_key=True)]
intfk = Annotated[int, mapped_column(init=False, nullable=False)]
created_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.now()),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
]


class Status(Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"


class Base(DeclarativeBase):
    metadata = metadata


@reg.mapped
class User(MappedAsDataclass, Base):
    """User class will be converted to a dataclass"""

    __tablename__ = "user_account"

    id: Mapped[intpk]
    name: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = column_property(firstname + " " + lastname)
    version: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    __mapper_args__ = {"version_id_col": version}


class Address(MappedAsDataclass, Base):
    __tablename__ = "address"

    id: Mapped[intpk]
    user_id: Mapped[intfk] = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str] = mapped_column()
    address_statistics: Mapped[Optional[str]] = mapped_column(Text, deferred=True)
    created_at: Mapped[created_at] = mapped_column()
    updated_at: Mapped[updated_at] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="addresses")


# class Parent(MappedAsDataclass, Base):
#     __tablename__ = "parent"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[List["Child"]] = relationship(default_factory=list, back_populates="parent")


# class Child(MappedAsDataclass, Base):
#     __tablename__ = "child"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
#     parent: Mapped["Parent"] = relationship(default=None)


# class User:
#     __tablename__ = "user"
#     __sa_dataclass_metadata_key__ = "sa"

#     id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
#     name: str = field(default=None, metadata={"sa": Column(String(50))})
#     fullname: str = field(default=None, metadata={"sa": Column(String(50))})
#     nickname: str = field(default=None, metadata={"sa": Column(String(12))})

#     addresses: List[Address] = field(default_factory=list, metadata={"sa": relationship("Address")})


# @mapper_registry.mapped
# @dataclass
# class Address:
#     __tablename__ = "address"
#     __sa_dataclass_metadata_key__ = "sa"

#     id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
#     user_id: int = field(init=False, metadata={"sa": Column(ForeignKey("user.id"))})
#     email_address: Optional[str] = field(default=None, metadata={"sa": Column(String(50))})


# engine = create_engine("sqlite:///:memory:")
# mapper_registry.metadata.create_all(bind=engine)

# user = User(name="Michael")
# user.addresses = [
#     Address(email_address="foo@bar.com"),
#     Address(email_address="bar@foo.com"),
# ]

with Session(engine, expire_on_commit=False) as session, session.begin():
    session.add(user)

print(user)
print(astuple(user))
print(json.dumps(asdict(user), indent=2))
