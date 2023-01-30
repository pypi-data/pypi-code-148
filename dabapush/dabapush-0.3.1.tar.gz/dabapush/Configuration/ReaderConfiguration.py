from pathlib import Path
from .PlugInConfiguration import PlugInConfiguration


class ReaderConfiguration(PlugInConfiguration):
    """ """

    yaml_tag = "!dabapush:ReaderConfiguration"

    def __init__(self, name, id, read_path: str or None, pattern: str or None) -> None:
        super().__init__(name, id=id)
        self.read_path = read_path if read_path is not None else "."
        self.pattern = pattern if pattern is not None else "*.json"

    def __repr__(self) -> str:
        return super().__repr__()
