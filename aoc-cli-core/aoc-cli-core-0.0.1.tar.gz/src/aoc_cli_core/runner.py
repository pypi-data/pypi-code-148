from pathlib import Path

class BaseRunner:
    def __init__(self, part: int, location: Path=None):
        if not location:
            location = Path()
        self._p = Path(location).absolute()
        self.part = part
        self.file = None
            
    def run(self) -> None:
        raise NotImplementedError
        