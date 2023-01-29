from pathlib import Path
import subprocess

from aoc_cli_core import BaseRunner

class Runner(BaseRunner):
    def __init__(self, part: int, location: Path=None):
        super().__init__(part, location)
        self.file = self._p / "main.go"
            
    def run(self) -> None:
        if self.file.exists() and self.file.is_file():
            try:
                output = subprocess.check_output(['go', 'run', self.file.resolve(), f"{self.part}"])
                answer = output.decode().strip().split("\n")[-1]
                print(f"Part {self.part}: {answer}")
                return answer
            except subprocess.CalledProcessError as e:
                print(e.stderr)
        else:
            raise AttributeError(f"Unable to run, perhaps it was unable to find 'main.go' within {self._p}.")

        