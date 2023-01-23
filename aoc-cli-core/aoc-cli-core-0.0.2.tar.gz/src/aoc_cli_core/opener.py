import webbrowser
from pathlib import Path

class BaseOpener:
    def __init__(self, location: Path=None) -> None:
        if not location:
            location = Path()
        self._p = Path(location).resolve()
        self.day: int = None
        self.year: int = None
        self.language: str = None
        self.validate()

    def validate(self):
        raise NotImplementedError      

    def open(self) -> None:
        if (self.day and self.year and self.language):
            self.url = f"https://adventofcode.com/2022/day/{self.day}"
            webbrowser.open(self.url)
        else:
            raise ValueError(f"Unable to ascertain required info 'year', 'language' and 'day' from path: {self._p.absolute()}")
        