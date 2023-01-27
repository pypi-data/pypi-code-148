# Seth --- Setting management library
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from abc import ABC
from dataclasses import _MISSING_TYPE, asdict, fields, is_dataclass
from typing import Any, Type, TypeVar

S = TypeVar("S", bound="Settings")


class SethException(Exception):
    pass


class NotADataclass(SethException):
    pass


class MissingValue(SethException):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name


class IncorrectValue(SethException):
    def __init__(self, name: str, value: str) -> None:
        super().__init__(f"'{name}': '{value}'")
        self.name = name
        self.value = value


class Settings(ABC):
    @classmethod
    def from_dict(cls: Type[S], data: dict[str, Any]) -> S:
        def value(field: Any) -> Any:
            # Value provided
            if field.name in data:
                try:
                    # Optional value
                    if (
                        hasattr(field.type, "__args__")
                        and len(field.type.__args__) == 2
                        and field.type.__args__[-1] is type(None)  # noqa
                    ):
                        return field.type.__args__[0](data[field.name])

                    return field.type(data[field.name])
                except Exception as exc:
                    raise IncorrectValue(field.name, str(exc))

            # Default value
            if not isinstance(field.default, _MISSING_TYPE):
                return field.default

            # Missing mandatory value
            raise MissingValue(field.name)

        if not is_dataclass(cls):
            raise NotADataclass(cls.__name__)
        return cls(**{f.name: value(f) for f in fields(cls)})

    @classmethod
    def to_dict(cls: Type[S], settings: "Settings") -> dict[str, Any]:
        return asdict(settings)
