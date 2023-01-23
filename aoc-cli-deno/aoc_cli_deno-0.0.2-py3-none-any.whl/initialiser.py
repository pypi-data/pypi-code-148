from pathlib import Path

from aoc_core_cli import BaseInitialiser

from .language import __language__


class Initialiser(BaseInitialiser):
    def __init__(self, year: int, location:Path=None):
        self.language = __language__
        self.year = year
        if location is None:
            location = Path()
        self.base_dir_location = Path(location) / f"{self.year}" / self.language
        self.set_file_content_template()

    def set_file_content_template(self):
        self.file_content = '''
const PROD = false;

const TEST_INPUT = ``

const INPUT =  PROD ? await Deno.readTextFile("./input.txt") : TEST_INPUT; 


function part1() {
    throw Error("NotImplemented");
}

function part2() {
    throw Error("NotImplemented");
}


function main() {
    const part = Deno.args[0];
    console.log(part)
    const parts = {
        '1': part1,
        '2': part2,
    }
    console.log(`Day: XXDAYXX Part: ${part}`);
    console.log(parts[part]());
}
main();
'''

    def initialise(self):
        print("[+] Scaffolding project...")
        self.mkdirs()
        self.mkdotenv()
        self.write_file_templates()
        print("[+] ...Done.")



    def write_file_templates(self):
        for i in range(1, 26):
            daily_file: Path = self.base_dir_location / f"{i:02}" / "day.js"
            daily_file.write_text(self.file_content.replace("XXDAYXX", f"{i}"))
        

