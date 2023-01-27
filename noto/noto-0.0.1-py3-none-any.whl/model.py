from pathlib import Path
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, Session
from sqlalchemy import Column, ForeignKey, String, Integer, Table


class Base(DeclarativeBase):
    pass


association_table = Table(
    "notes_tags",
    Base.metadata,
    Column("note_id", ForeignKey("note.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: str = Column(String, unique=True)

    def __repr__(self) -> str:
        return self.name


class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: str = Column(String)
    priority: int = Column(Integer)

    tags: Mapped[list[Tag]] = relationship(
        "Tag", secondary=association_table, backref="notes", lazy=False
    )

    def upsert_tags(self, session: Session, tags: list[str], remove: bool = False):
        for name in tags:
            tag = session.query(Tag).filter_by(name=name).scalar()
            if tag is None:
                tag = Tag(name=name)

            if remove:
                if tag in self.tags:
                    self.tags.remove(tag)
            else:
                self.tags.append(tag)

    def __repr__(self) -> str:
        return f"""Note(id={self.id}, text={self.text}{f", priority={self.priority}" if self.priority != 0 else ""}{f", tags={self.tags}" if len(self.tags) > 0 else ""})"""


from sqlalchemy import create_engine

noto_home = str(Path.home() / ".noto")
engine = create_engine("sqlite:////" + str(Path(noto_home) / 'db.sqlite'), echo=False, future=True)
Base.metadata.create_all(engine)
