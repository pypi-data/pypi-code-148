from importlib.machinery import SourceFileLoader
from pathlib import Path

from aoc_cli_core import BaseRunner

class Runner(BaseRunner):
    def __init__(self, part: int, location: Path=None):
        super().__init__(part, location)
        self.file = self._p / "day.py"
            
    def run(self) -> None:
        if self.file.exists() and self.file.is_file():
            module = SourceFileLoader('day', str(self.file.resolve())).load_module()
            answer = module.part_1() if self.part == 1 else module.part_2()
            print(f"Part {self.part}: {answer}")
            return answer
        else:
            raise AttributeError(f"Unable to run, perhaps it was unable to find 'day.py' within {self._p}.")

        