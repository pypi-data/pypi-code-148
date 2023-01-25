from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class User:
    __tablename__ = "user"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(default=None, metadata={"sa": Column(String(50))})
    fullname: str = field(default=None, metadata={"sa": Column(String(50))})
    nickname: str = field(default=None, metadata={"sa": Column(String(12))})

    addresses: List[Address] = field(default_factory=list, metadata={"sa": relationship("Address")})


@mapper_registry.mapped
@dataclass
class Address:
    __tablename__ = "address"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    user_id: int = field(init=False, metadata={"sa": Column(ForeignKey("user.id"))})
    email_address: Optional[str] = field(default=None, metadata={"sa": Column(String(50))})


engine = create_engine("sqlite:///:memory:")
mapper_registry.metadata.create_all(bind=engine)

user = User(name="Michael")
user.addresses = [
    Address(email_address="foo@bar.com"),
    Address(email_address="bar@foo.com"),
]

with Session(engine, expire_on_commit=False) as session, session.begin():
    session.add(user)

print(user)
print(astuple(user))
print(json.dumps(asdict(user), indent=2))
