from importlib.machinery import SourceFileLoader
from pathlib import Path

from aoc_cli_core import BaseSubmitter
from aoc_cli_core.validations import is_valid_day, is_valid_year

from .local_validations import is_valid_language

class Submitter(BaseSubmitter):
    def __init__(self, part: int, location: Path=None):
        super().__init__(part, location)

    def validate(self):
        if is_valid_day(self._p.name):
            self.day = int(self._p.name)
        for x in self._p.parents:
            if is_valid_day(x.name):
                self.day = int(x.name)
                continue
            if is_valid_language(x.name) and is_valid_year(x.parent.name):
                self.year = int(x.parent.name)
                self.language = x.name
                break
        if (self.day and self.year and self.language):
            self.file = self._p / "day.py"
        else:
            raise ValueError(f"Unable to ascertain required info 'year', 'language' and 'day' from path: {self._p.resolve()}")

    def devise_answer(self):
        day_module = SourceFileLoader('day', str(self.file.resolve())).load_module()
        if hasattr(day_module, "PROD") and not day_module.PROD:
            raise ValueError(f"[!] Attempted to submit without PROD flag set to True. As a precaution this is disabled.")
        try:
            self.answer = day_module.part_1() if self.part == 1 else day_module.part_2()
        except NotImplementedError:
            print(f"[!] NotImplementedError raised. Perhaps you have attempted to submit an incomplete answer?")
        

   