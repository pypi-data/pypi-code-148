import inspect
import os
import pathlib
from typing import Union, Iterable, List

from rshanker779_common.logger import get_logger

logger = get_logger(__name__)


class Path:
    def __init__(self, *paths: Union[str, pathlib.Path]):
        self.path = pathlib.Path(*paths)

    def __getattr__(self, item: str):
        return getattr(self.path, item)

    def ls(self) -> List:
        return [self.__class__(p) for p in self.path.glob("*")]

    def __dir__(self) -> Iterable[str]:
        return super().__dir__() + dir(self.path)

    def __truediv__(self, other):
        return self.__class__(self.path / other)

    def make_dirs(self):
        self.mkdir(parents=True, exist_ok=True)
        return self


def relative_path(*args: str) -> Path:
    frame = inspect.stack()[1]
    file_path = Path(frame.filename)
    return Path(file_path.parent, *args)


def make_dirs(directory: Union[str, bytes]) -> Path:
    return Path(directory).make_dirs()


def add_init_files(filepath: Union[str, bytes, pathlib.Path]):
    for root, _, files in os.walk(Path(filepath).path):
        needs_init_file = any(i for i in files if i.endswith(".py") and i != "setup.py")
        has_init_file = any(i for i in files if i == "__init__.py")
        if needs_init_file and not has_init_file:
            logger.info("Adding init file to directory %s", root)
            Path(root, "__init__.py").write_text("")
