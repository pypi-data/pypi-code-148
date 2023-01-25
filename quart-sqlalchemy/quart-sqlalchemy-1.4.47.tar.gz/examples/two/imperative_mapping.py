# from __future__ import annotations

# from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

import anyio
from pydantic.dataclasses import dataclass
from quart import Quart
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload

from quart_sqlalchemy import SQLAlchemy


registry = registry()

app = Quart(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
db = SQLAlchemy(app, metadata=registry.metadata)


@dataclass
class User:
    id: Optional[int] = field(init=False, default=None)
    name: Optional[str] = None
    fullname: Optional[str] = None
    nickname: Optional[str] = None
    addresses: List["Address"] = field(default_factory=list)


@dataclass
class Address:
    id: Optional[int] = field(init=False, default=None)
    user_id: Optional[int] = field(init=False, default=None)
    email_address: Optional[str] = None


User.__pydantic_model__.update_forward_refs()

user = Table(
    "user",
    registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

address = Table(
    "address",
    registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
)

registry.map_imperatively(
    User,
    user,
    properties={
        "addresses": relationship(Address, backref="user", order_by=address.c.id),
    },
)

registry.map_imperatively(Address, address)


async def main():
    async with app.app_context():
        db.create_all()

        user = User(
            "joe",
            "Joe Black",
            "Joe",
            [Address(email_address="joe@joe.com")],
        )
        with db.session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            session.expunge(user)

        # print(user)
        import pdb

        pdb.set_trace()

        with db.session() as session:
            statement = select(User).where(User.name == "joe").options(selectinload(User.addresses))
            model = session.execute(statement).scalars().one()
            assert model.id == user.id


anyio.run(main)
