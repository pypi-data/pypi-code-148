from __future__ import annotations

import typing as t
from copy import copy

from markupsafe import Markup

from .fields import Field
from .utils import render_error


__all__ = ("Form", "SEP")

SEP = "--"


class Form:
    error: str | None = None
    updated_fields: list[str] | None = None
    prefix: str = ""

    _model: t.Any = None
    _is_valid: bool | None = None
    _valid_data: dict[str, t.Any] | None = None
    _fields: list[str] | None = None

    def __init__(
        self,
        input_data=None,
        object=None,
        file_data=None,
        *,
        prefix="",
    ):
        self.prefix = prefix or ""
        self._setup_fields()
        self.load_data(input_data, object, file_data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.prefix})"

    def load_data(
        self,
        input_data: dict | None = None,
        object: t.Any = None,
        file_data: dict | None = None,
    ) -> None:
        self._is_valid = None
        self._valid_data = None
        self.updated_fields = None

        if isinstance(input_data, dict):
            input_data = FakeMultiDict(input_data)
        if input_data is None:
            input_data = FakeMultiDict()

        if isinstance(file_data, dict):
            file_data = FakeMultiDict(file_data)
        if file_data is None:
            file_data = FakeMultiDict()

        object = object or {}
        if isinstance(object, dict) or not object:
            self._object = None
        else:
            self._object = object

        self._load_field_data(input_data, object, file_data)

    def render_error(self, tag: str = "div", **attrs) -> Markup:
        return render_error(self.error, tag=tag, **attrs)

    def validate(self) -> dict[str, t.Any] | None:  # noqa: C901
        if self._is_valid is False:
            return None
        if self._valid_data is not None:
            return self._valid_data

        self.error = None
        is_valid = True
        updated = []
        valid_data = {}

        for name in self._fields or []:
            field = getattr(self, name)
            py_value = field.validate()

            if field.error:
                is_valid = False
                self.error = field.error
                continue

            valid_data[name] = py_value
            if field.updated:
                updated.append(name)

        self._is_valid = is_valid
        if is_valid:
            self._valid_data = valid_data
            self.updated_fields = updated
            return valid_data

    def save(self, **data) -> t.Any:
        if not self.validate():
            return None

        if self._valid_data:
            data.update(self._valid_data)
        if not self._model:
            return data

        if self._object:
            return self.update_object(data)
        return self.create_object(data)

    def create_object(self, data: dict[str, t.Any]) -> t.Any:
        assert self._model
        return self._model(**data)

    def update_object(self, data: dict[str, t.Any]) -> t.Any:
        for key, value in data.items():
            setattr(self._object, key, value)
        return self._object

    def _setup_fields(self) -> None:
        fields = []
        attrs = (
            "updated_fields",
            "prefix",
            "load_data",
            "validate",
            "save",
            "create_object",
            "update_object",
            "get_db_session",
        )
        for name in dir(self):
            if name.startswith("_") or name in attrs:
                continue
            attr = getattr(self, name)

            if isinstance(attr, Field):
                self._setup_field(attr, name)
                fields.append(name)

        self._fields = fields

    def _setup_field(self, field: Field, name: str) -> None:
        field = copy(field)
        setattr(self, name, field)
        if self.prefix:
            field.name = self.prefix + SEP + name
        else:
            field.name = name
        if field.custom_prepare is None:
            field.custom_prepare = getattr(self, "prepare_" + name, None)
        if field.custom_clean is None:
            field.custom_clean = getattr(self, "clean_" + name, None)

    def _load_field_data(
        self, input_data: dict[str, t.Any], object: t.Any, file_data: dict[str, t.Any]
    ) -> None:
        for name in self._fields or []:
            field = getattr(self, name)
            full_name = field.name
            input_values = get_input_values(input_data, full_name) or get_input_values(
                file_data, full_name
            )
            object_value = get_object_value(object, name)
            field.load_data(input_values, object_value)


class FakeMultiDict(dict):
    def getall(self, name: str) -> list[str]:
        if name not in self:
            return []
        return [self[name]]


def get_input_values(data: t.Any, name: str) -> t.Sequence[str]:
    # - WebOb, Bottle, and Proper uses `getall`
    # - Django, Flask (Werkzeug), cgi.FieldStorage, etc. uses `getlist`
    # - CherryPy just gives you a dict with lists or values
    values = []
    if hasattr(data, "getall"):
        values = data.getall(name)
    if hasattr(data, "getlist"):
        values = data.getlist(name)
    else:
        values = data.get(name)

    # Some frameworks, like CherryPy, don't have a special method for
    # always returning a list of values.
    if values is None:
        return []
    if not isinstance(values, (list, tuple)):
        return [values]
    return values


def get_object_value(obj: t.Any, name: str) -> t.Any:
    # The object could be a also a dictionary
    # The field name could conflict with a native method
    # if `obj` is a dictionary instance
    if isinstance(obj, dict):
        return obj.get(name, None)
    return getattr(obj, name, None)
