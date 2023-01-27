from noto.model import engine, Note, Tag
from sqlalchemy import select
from sqlalchemy.orm import Session
from random import sample


def read(
    amount: int, min_priority: int, max_priority: int, random: bool, tags: list[str]
) -> list[Note]:

    # amount=None will return all values
    if amount < 0:
        amount = None

    with Session(engine) as session:
        stmt = select(Note).order_by(Note.priority)
        conditions = []
        if min_priority:
            conditions.append(Note.priority >= min_priority)
        if max_priority:
            conditions.append([Note.priority <= max_priority])
        if tags:
            conditions.append(Note.tags.any(Tag.name.in_(tags)))
        notes = session.scalars(stmt.where(*conditions)).unique().all()

        if notes:
            if random and amount:
                return sample(notes, k=amount)
            else:
                return notes[:amount]
        else:
            return []
