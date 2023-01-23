# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prosemirror',
 'prosemirror.model',
 'prosemirror.schema.basic',
 'prosemirror.schema.list',
 'prosemirror.test_builder',
 'prosemirror.transform']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'prosemirror',
    'version': '0.3.2',
    'description': 'Python implementation of core ProseMirror modules for collaborative editing',
    'long_description': '# prosemirror-py\n\n[![CI](https://github.com/fellowapp/prosemirror-py/actions/workflows/test.yml/badge.svg)](https://github.com/fellowapp/prosemirror-py/actions/workflows/test.yml)\n[![Code Coverage](https://codecov.io/gh/fellowapp/prosemirror-py/branch/master/graph/badge.svg?style=flat)](https://codecov.io/gh/fellowapp/prosemirror-py)\n[![Python Version](https://img.shields.io/pypi/pyversions/prosemirror.svg?style=flat)](https://pypi.org/project/prosemirror/)\n[![PyPI Package](https://img.shields.io/pypi/v/prosemirror.svg?style=flat)](https://pypi.org/project/prosemirror/)\n[![License](https://img.shields.io/pypi/l/prosemirror.svg?style=flat)](https://github.com/fellowapp/prosemirror-py/blob/master/LICENSE.md)\n[![Fellow Careers](https://img.shields.io/badge/fellow.app-hiring-576cf7.svg?style=flat)](https://fellow.app/careers/)\n\nThis package provides Python implementations of the following\n[ProseMirror](https://prosemirror.net/) packages:\n\n- [`prosemirror-model`](https://github.com/ProseMirror/prosemirror-model) version 1.18.1\n- [`prosemirror-transform`](https://github.com/ProseMirror/prosemirror-transform) version 1.6.0\n- [`prosemirror-test-builder`](https://github.com/ProseMirror/prosemirror-test-builder)\n- [`prosemirror-schema-basic`](https://github.com/ProseMirror/prosemirror-schema-basic) version 1.1.2\n- [`prosemirror-schema-list`](https://github.com/ProseMirror/prosemirror-schema-list)\n\nThe original implementation has been followed as closely as possible during\ntranslation to simplify keeping this package up-to-date with any upstream\nchanges.\n\n## Why?\n\nProseMirror provides a powerful toolkit for building rich-text editors, but it\'s\nJavaScript-only. Until now, the only option for manipulating and working with\nProseMirror documents from Python was to embed a JS runtime. With this\ntranslation, you can now define schemas, parse documents, and apply transforms\ndirectly via a native Python API.\n\n## Status\n\nThe full ProseMirror test suite has been translated and passes. This project\nonly supports Python 3. There are no type annotations at the moment, although\nthe original has annotations available in doc comments.\n\n## Usage\n\nSince this library is a direct port, the best place to learn how to use it is\nthe [official ProseMirror documentation](https://prosemirror.net/docs/guide/).\nHere is a simple example using the included "basic" schema:\n\n```python\nfrom prosemirror.transform import Transform\nfrom prosemirror.schema.basic import schema\n\n# Create a document containing a single paragraph with the text "Hello, world!"\ndoc = schema.node("doc", {}, [\n    schema.node("paragraph", {}, [\n        schema.text("Hello, world!")\n    ])\n])\n\n# Create a Transform which will be applied to the document.\ntr = Transform(doc)\n\n# Delete the text from position 3 to 5. Adds a ReplaceStep to the transform.\ntr.delete(3, 5)\n\n# Make the first three characters bold. Adds an AddMarkStep to the transform.\ntr.add_mark(1, 4, schema.mark("strong"))\n\n# This transform can be converted to JSON to be sent and applied elsewhere.\nassert [step.to_json() for step in tr.steps] == [{\n    \'stepType\': \'replace\',\n    \'from\': 3,\n    \'to\': 5\n}, {\n    \'stepType\': \'addMark\',\n    \'mark\': {\'type\': \'strong\', \'attrs\': {}},\n    \'from\': 1,\n    \'to\': 4\n}]\n\n# The resulting document can also be converted to JSON.\nassert tr.doc.to_json() == {\n    \'type\': \'doc\',\n    \'content\': [{\n        \'type\': \'paragraph\',\n        \'content\': [{\n            \'type\': \'text\',\n            \'marks\': [{\'type\': \'strong\', \'attrs\': {}}],\n            \'text\': \'Heo\'\n        }, {\n            \'type\': \'text\',\n            \'text\': \', world!\'\n        }]\n    }]\n}\n```',
    'author': 'Shen Li',
    'author_email': 'shen@fellow.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fellowinsights/prosemirror-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
