from datetime import datetime

from meiki.NoteType import NoteType

"""
    The SimpleNote only implements the
    base metadata of the note.
    
    The body/content should be implemented by the
    child classes to prevent polymorphic behavior
    where an audio note is read as text file
"""


class BaseNote:

    def __init__(self):
        self._title = None
        self._created_on = datetime.now()
        self._updated_on = datetime.now()
        self._note_type = NoteType.BASE_NOTE

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def note_type(self) -> NoteType:
        return self._note_type

    @note_type.setter
    def note_type(self, note_type: NoteType) -> None:
        self._note_type = note_type
