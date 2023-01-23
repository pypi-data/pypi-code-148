"""
    NoteType Constants

    All note MUST include their TYPE so the consumer can
    change behavior depending on the type given

    When Creating a child class, a new type MUST be created
    and appended at the end of the file no matter how similar
    it is with an existing note type.
"""
from enum import Enum


class NoteType(Enum):
    BASE_NOTE = 'BaseNote'

    ANIME_NOTE = 'AnimNote'
