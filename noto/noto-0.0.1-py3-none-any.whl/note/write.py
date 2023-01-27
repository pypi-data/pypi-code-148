from noto.model import engine, Note, Tag
from sqlalchemy import select
from sqlalchemy.orm import Session


def write(text: str, priority: int, tags: list[str]) -> list[Note]:
    with Session(engine) as session:
        note = Note(text=text, priority=priority)
        note.upsert_tags(session=session, tags=tags or [], remove=False)

        session.add(note)
        session.commit()

        return [session.get(Note, note.id)]
