from BaseNote import BaseNote
from NoteType import NoteType


class AnimeNote(BaseNote):

    def __init__(self):
        super().__init__()
        self._note_type = NoteType.ANIME_NOTE

        self._japanese_title = None
        self._english_title = None
        self._romaji_title = None
        self._rating = 0

    @property
    def japanese_title(self) -> str:
        return self._japanese_title

    @japanese_title.setter
    def japanese_title(self, title: str) -> None:
        self._japanese_title = title

        # Only set the Japanese title if it's blank (no english title)
        if self._title is None:
            self._title = title

    @property
    def romaji_title(self) -> str:
        return self._romaji_title

    @romaji_title.setter
    def romaji_title(self, title) -> None:
        self._romaji_title = title

        # Romaji should be our last resort for title
        if self._title is None and self._japanese_title is None:
            self._title = title

    @property
    def english_title(self) -> str:
        return self._english_title

    @english_title.setter
    def english_title(self, title) -> None:
        self._english_title = title

        # Always override the title to english
        self._title = title
