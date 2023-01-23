import os
import requests
from pathlib import Path

class BaseSubmitter:
    def __init__(self, part: int, location: Path=None):
        if not location:
            location = Path()
        self._p = Path(location).resolve()
        self.part = part
        self.day: int = None
        self.year: int = None
        self.language: str = None
        self.answer = None
        self.validate()        
    
    def validate(self):
        raise NotImplementedError
        
    def submit(self) -> None:
        if self.file.exists() and self.file.is_file():
            self.devise_answer()
            self.submit_answer()
        else:
            raise ValueError(f"{self._p.resolve()} not found or not a file.")
        

    def devise_answer(self):
        raise NotImplementedError

    def submit_answer(self):
        if self.answer:
            session_cookie = os.environ['AOC_SESSION']
                
            url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"
            cookies = dict(session=session_cookie)
            headers = {"User-Agent": "github.com/emilkloeden/aoc"}
            data = {
                "submit": "[Submit]",
                "answer": self.answer,
                "level": self.part
            }
            r = requests.post(url, data=data, cookies=cookies, headers=headers)
            if r.status_code == 200:
                if "That's the right answer!" in r.text:
                    print(f"[*] Your answer to part {self.part} ({self.answer}) was correct!")
                else:
                    print(f"[-] That probably wasn't correct, see ressponse below\n")
                    print(r.text)
            else:
                print(f"[!] {r.status_code} status code returned.")
        else:
            print(f"[!] No answer returned from part {part}.")
        
        