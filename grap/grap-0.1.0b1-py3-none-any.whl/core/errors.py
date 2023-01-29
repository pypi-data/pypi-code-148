from __future__ import annotations

class ParseError(Exception):
    def __init__(self, message: str, location: int):
        self.message = message
        self.location = location
        super().__init__(message)

