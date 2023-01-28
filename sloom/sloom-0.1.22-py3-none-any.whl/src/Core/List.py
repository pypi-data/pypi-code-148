import functools
from .Terminal import *

class List:
    """
    Type safe collection with custom functions
    Includes:
    - reduce, filter, map
    """
    def __init__(self, type) -> None:
        self.contents = []
        self.type = type
        pass

    def append(self, value):
        if isinstance(value, self.type):
            self.contents.append(value)
        else:
            Terminal.error(f"Type mismatch:{type(value)} is not {type}")

    def filter(self, fn):
        self.contents = filter(fn, self.contents)

    def map(self, fn):
        self.contents = map(fn, self.contents)

    def reduce(self, fn):
        return functools.reduce(fn, self.contents)
    
    def count(self):
        return len(self.contents)
    
