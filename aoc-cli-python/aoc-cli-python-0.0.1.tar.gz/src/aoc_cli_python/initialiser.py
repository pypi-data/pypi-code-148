from pathlib import Path

from aoc_core import BaseInitialiser

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
        self.file_content = '''import argparse
from pathlib import Path

PROD = False

def load_input():
    return (Path() / "input.txt").read_text()

TEST_INPUT = """
"""

INPUT = load_input() if PROD else TEST_INPUT


def part_1() -> str:
    raise NotImplementedError

def part_2() -> str:
    raise NotImplementedError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int, choices=(1,2))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parts = {
        1: part_1,
        2: part_2,
    }
    print(f"Day: XXDAYXX Part: {args.part}")
    print(parts[args.part]())

if __name__ == "__main__":
    main()
'''

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
        

