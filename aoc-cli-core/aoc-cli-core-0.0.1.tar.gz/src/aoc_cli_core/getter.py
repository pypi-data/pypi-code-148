import os
from pathlib import Path

import requests

class BaseGetter:
    def __init__(self, location: Path=None):
        self.day: int = None
        self.year: int = None
        self.language: str = None
        if location is None:
            location = Path()
        self._p = Path(location).resolve()
        self.validate()

    def validate(self):
        raise NotImplementedError

    def get_input(self):
        try:
            session_cookie = os.environ['AOC_SESSION']
            
            url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
            cookies = dict(session=session_cookie)
            headers = {"User-Agent": "github.com/emilkloeden/aoc"}
            
            r = requests.get(url, cookies=cookies, headers=headers)
            self.input_file_location.write_text(r.text)
        except KeyError:
            print("[!] Unable to get input, AOC_SESSION environment variable not set")
        except AttributeError:
            print("[!] Unable to save input, perhaps location was not set/set incorrectly")