from pathlib import Path
from typing import Protocol

class InitialiserProtocol(Protocol):
    def initialise(self):
        pass

    def mkdirs(self):
        pass

    def write_file_templates(self):
        pass

class BaseInitialiser(InitialiserProtocol):
    def __init__(self, year: int, location:Path=None):
        self.language = None
        self.year = year
        if location is None:
            location = Path()
        if not self.language:
            raise ValueError("No language set.")
        self.base_dir_location = Path(location) / f"{self.year}" / self.language

        self.set_file_content_template()

    def initialise(self):
        raise NotImplementedError

    def mkdotenv(self):
        dotenv_path = self.base_dir_location / ".env"
        dot_env_contents = """# AOC Environment Variables
#AOC_SESSION= # Required to download input files
"""
        dotenv_path.write_text(dot_env_contents)

    def mkdirs(self):
        try:
            self.base_dir_location.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f"{self.base_dir_location.absolute()} exists, ignoring...")
        for i in range(1, 26):
            try:
                subdir = self.base_dir_location / f"{i:02}"
                subdir.mkdir(exist_ok=False)
            except FileExistsError:
                print(f"{subdir.absolute()} exists, ignoring...")


    def write_file_templates(self):
        raise NotImplementedError
        

