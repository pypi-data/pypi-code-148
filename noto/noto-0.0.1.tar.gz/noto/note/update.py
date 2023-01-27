from noto.model import Tag, engine, Note
from sqlalchemy.orm import Session


def update(
    id: int,
    text: str = None,
    priority: str = None,
    add_tags: list[str] = [],
    remove_tags: list[str] = [],
) -> list[Note]:
    with Session(engine) as session:
        note = session.get(Note, id)
        if add_tags is not None:
            note.upsert_tags(session=session, tags=add_tags, remove=False)
        if remove_tags is not None:
            note.upsert_tags(session=session, tags=remove_tags, remove=True)
        if text is not None:
            note.text = text
        if priority is not None:
            note.priority = priority

        session.add(note)
        session.commit()

        return [session.get(Note, note.id)]
