from __future__ import annotations

import json

from episteme._app import app
from episteme._credentials import creds
from episteme._manifests import get_manifests
from episteme._model import Model
from episteme._model import ModelInvalid

with open('./tests/manifests.json') as f:
    get_manifests().update(json.load(f))


def main() -> None:
    try:
        print(creds('db', 'aff'))

        t = Model('todo', {'title': 'code episteme', 'completed': True})
        t.save()
        f = Model.find('todo', t._get('id'))
        print(f)
        f._set('title', 'code episteme updated')
        f.save()
        print(app().get_all())

        # t.set('title','co')
    except ModelInvalid as e:
        print(e)
        for k, errors in t.validation_errors().items():
            for error in errors:
                print(f'{k}: {error}')

# https://alpinejs.dev/
