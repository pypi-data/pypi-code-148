from json.decoder import JSONDecodeError
from typing import TypeVar, Callable, Union
from pathlib import Path
from dataclasses_json import DataClassJsonMixin
from .storage import read_from_drive, save_to_drive

T = TypeVar('T', bound=DataClassJsonMixin)


def empty_settings(Settings: Callable[[], T], path: Union[str, Path]) -> T:
    settings = Settings()
    save_to_drive(settings.to_json(), path)
    return settings


def get_settings(Settings: Callable[[], T], path: Union[str, Path]) -> T:
    try:
        settings = read_from_drive(path)
        return Settings().from_json(settings)
    except (FileNotFoundError, JSONDecodeError):
        return empty_settings(Settings, path)
