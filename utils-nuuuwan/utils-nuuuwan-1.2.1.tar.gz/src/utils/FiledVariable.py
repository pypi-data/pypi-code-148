from functools import cached_property

from utils.File import JSONFile


class FiledVariable:
    def __init__(self, key: str, func_get):
        self.key = key
        self.func_get = func_get

    @property
    def file_path(self):
        return f'/tmp/{self.key}.json'

    @property
    def file(self):
        return JSONFile(self.file_path)

    def clear(self):
        self.file.delete()

    @cached_property
    def value(self):
        if self.file.exists:
            return self.file.read()
        else:
            value = self.func_get()
            self.file.write(value)
            return value
