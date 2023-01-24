import json
import os.path
from pathlib import Path
from typing import Union, Type, TypeVar

from configj.abstract_config import AbstractConfig

T = TypeVar('T', bound=AbstractConfig)


class ConfigJ:

    def __init__(self, file_path: Union[str, Path], target_class: Type[T]) -> None:
        self.file_path = file_path
        self.target_class = target_class

    def load(self):
        if not os.path.exists(self.file_path):
            obj = self.target_class()
            self.save(obj)
            return obj

        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        obj = self.target_class()  # type: T
        keys = self.target_class.__dict__.keys()

        for key in keys:
            if not key.startswith('_'):
                if key in data:
                    value = data[key]
                    setattr(obj, key, value)

        return obj

    def save(self, config: T):
        keys = self.target_class.__dict__.keys()
        data = {}
        for key in keys:
            if not key.startswith('_'):
                value = getattr(config, key)
                data[key] = value
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


