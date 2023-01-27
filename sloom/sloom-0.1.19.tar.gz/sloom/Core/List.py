import functools
from .Terminal import *

class List:
    """
    Type safe collection with custom functions
    Includes:
    - reduce, filter, map
    """
    def __init__(self, type) -> None:
        self.contents = list()
        self.type = type
        pass

    def append(self, value):
        if isinstance(value, self.type):
            self.contents.append(value)
        else:
            Terminal.error(f"Type mismatch:{type(value)} is not {self.type}")
            raise TypeError

    def extend(self, iterator):
        for i in iterator:
            self.append(i)
    
    def filter(self, fn):
        self.contents = list(filter(fn, self.contents))

    def map(self, fn):
        self.contents = list(map(fn, self.contents))

    def reduce(self, fn):
        return functools.reduce(fn, self.contents)
    
    def count(self):
        return len(self.contents)

    def first(self):
        try: 
            return self.contents[0]
        except:
            return None
    
    def __str__(self) -> str:
        text = "" + "["
        spacer = ", "
        for i in self.contents:
            text += i + spacer
        text = text.removesuffix(spacer)
        text += "]"
        return text