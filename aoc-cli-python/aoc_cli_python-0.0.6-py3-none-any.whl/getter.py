from aoc_cli_core import BaseGetter
from aoc_cli_core.validations import is_valid_day, is_valid_year

from .local_validations import is_valid_language

class Getter(BaseGetter):
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
            self.input_file_location = self._p / "input.txt"
        else:
            raise ValueError(f"Unable to ascertain required info 'year', 'language' and 'day' from path: {self._p}")
