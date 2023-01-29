from pathlib import Path
import subprocess

from aoc_cli_core import BaseRunner

class Runner(BaseRunner):
    def __init__(self, part: int, location: Path=None):
        super().__init__(part, location)
        self.file = self._p / "day.js"
            
    def run(self) -> None:
        if self.file.exists() and self.file.is_file():
            output = subprocess.check_output(['deno', 'run', '--allow-read', self.file.resolve(), f"{self.part}"])
            answer = output.decode().strip().split("\n")[-1]
            print(f"Part {self.part}: {answer}")
            return answer
        else:
            raise AttributeError(f"Unable to run, perhaps it was unable to find 'day.js' within {self._p}.")

        