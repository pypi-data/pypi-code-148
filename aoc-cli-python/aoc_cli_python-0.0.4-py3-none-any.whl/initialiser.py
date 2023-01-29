from pathlib import Path

# We require python 3.10, so this is fine.
from importlib.resources import files

from aoc_cli_core import BaseInitialiser

from .language import __language__

class Initialiser(BaseInitialiser):
    def __init__(self, year: int, location: Path=None):
        self.language = __language__
        self.year = year
        if location is None:
            location = Path()
        self.base_dir_location = Path(location) / f"{self.year}" / self.language
        self.set_file_content_template()

    def set_file_content_template(self):
        resources = files("aoc_cli_go")
        self.file_content = (resources / "resources" / "day.py").read_text()


    def initialise(self):
        print("[+] Scaffolding project...")
        self.mkdirs()
        self.mkdotenv()
        self.write_file_templates()
        print("[+] ...Done.")



    def write_file_templates(self):
        for i in range(1, 26):
            daily_file: Path = self.base_dir_location / f"{i:02}" / "day.py"
            daily_file.write_text(self.file_content.replace("XXDAYXX", f"{i}"))
        

