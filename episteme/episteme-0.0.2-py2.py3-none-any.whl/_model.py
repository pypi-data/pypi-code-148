from __future__ import annotations

from typing import Any

from cerberus import Validator

from episteme._database import get_db
from episteme._manifests import get_manifests
from episteme._utils import dget
from episteme._utils import dset
from episteme._utils import ulid


# https://docs.python-cerberus.org/en/stable/usage.html#basic-usage


class ModelNotFound(Exception):
    pass


class ModelInvalid(Exception):
    pass


db = {}
# db = None

m = get_manifests()


class Model:
    _PK = 'id'
    v = Validator({}, allow_unknown={'type': 'string'})

    def __init__(self, model_name, data) -> None:
        if model_name not in m.fetch('models'):
            raise ModelInvalid('model not found')
        self.model_name = model_name
        self.data = data
        self.validate()

    def validate(self):
        schema = dget(m.fetch('models'), f'{self.model_name}.schema')
        if not self.v.validate(self.data, schema):
            raise ModelInvalid()

    def validation_errors(self):
        return self.v.errors

    def _set(self, k: str, v: Any):
        dset(self.data, k, v)
        self.validate()

    def _get(self, k: str, default=None) -> Any:
        return dget(self.data, k, default)

    def save(self):

        db = get_db()

        id = self._get(self._PK, None)

        if id is None:
            id = ulid()
            self._set(self._PK, id)
            db.insert(self.model_name, self.data.copy(), self._PK)
        else:
            db.update(self.model_name, self.data.copy(), self._PK)

    def find(model_name: str, id: str):

        db = get_db()
        result = db.find(model_name, id, Model._PK)
        if result is None:
            raise ModelNotFound()
        return Model(model_name, result)

    def where(self, query=[]):
        pass

    def __str__(self) -> str:
        return f'Model({self.model_name})::{self.data.__str__()}'
