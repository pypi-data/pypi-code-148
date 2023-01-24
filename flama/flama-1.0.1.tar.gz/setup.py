# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flama',
 'flama.cli',
 'flama.cli.commands',
 'flama.cli.config',
 'flama.codecs',
 'flama.codecs.http',
 'flama.codecs.websockets',
 'flama.debug',
 'flama.injection',
 'flama.models',
 'flama.models.models',
 'flama.pagination',
 'flama.resources',
 'flama.schemas',
 'flama.schemas._libs',
 'flama.schemas._libs.marshmallow',
 'flama.schemas._libs.pydantic',
 'flama.schemas._libs.typesystem',
 'flama.serialize',
 'flama.serialize.serializers',
 'flama.types']

package_data = \
{'': ['*'],
 'flama': ['templates/debug/*', 'templates/schemas/*'],
 'flama.cli': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1,<9.0',
 'pyyaml>=6.0,<7.0',
 'starlette>=0.21.0,<1.0.0',
 'uvicorn>=0.19,<0.20']

extras_require = \
{':python_version < "3.10"': ['typing-extensions>=4.4,<5.0'],
 ':python_version < "3.8"': ['importlib-metadata>=4.2,<5.0'],
 'database': ['SQLAlchemy[asyncio]>=1.4,<2.0'],
 'full': ['pydantic>=1.10,<2.0',
          'marshmallow>=3.0,<4.0',
          'python-forge>=18.6,<19.0',
          'apispec>=6.0,<7.0',
          'typesystem>=0.4.1,<0.5.0',
          'SQLAlchemy[asyncio]>=1.4,<2.0'],
 'marshmallow': ['marshmallow>=3.0,<4.0', 'apispec>=6.0,<7.0'],
 'pagination': ['python-forge>=18.6,<19.0'],
 'pydantic': ['pydantic>=1.10,<2.0'],
 'typesystem': ['typesystem>=0.4.1,<0.5.0']}

entry_points = \
{'console_scripts': ['flama = flama.cli.__main__:cli']}

setup_kwargs = {
    'name': 'flama',
    'version': '1.0.1',
    'description': 'Fire up your models with the flame 🔥',
    'long_description': '<p align="center">\n    <a href="https://flama.dev"><img src="https://raw.githubusercontent.com/perdy/flama/master/docs/images/logo.png" alt=\'Flama\'></a>\n</p>\n<p align="center">\n    <em>Fire up your models with the flame</em> &#128293;\n</p>\n<p align="center">\n    <a href="https://github.com/perdy/flama/actions">\n        <img src="https://github.com/perdy/flama/workflows/Test%20And%20Publish/badge.svg" alt="Test And Publish workflow status">\n    </a>\n    <a href="https://github.com/perdy/flama/actions">\n        <img src="https://github.com/perdy/flama/workflows/Docker%20Push/badge.svg" alt="Docker Push workflow status">\n    </a>\n    <a href="https://codecov.io/gh/perdy/flama">\n        <img src="https://codecov.io/gh/perdy/flama/branch/master/graph/badge.svg" alt="Coverage">\n    </a>\n    <a href="https://pypi.org/project/flama/">\n        <img src="https://img.shields.io/pypi/v/flama?logo=PyPI&logoColor=white" alt="Package version">\n    </a>\n    <a href="https://pypi.org/project/flama/">\n        <img src="https://img.shields.io/pypi/pyversions/flama?logo=Python&logoColor=white" alt="PyPI - Python Version">\n    </a>\n</p>\n\n---\n\n# Flama\n\nFlama is a python library which establishes a standard framework for\ndevelopment and deployment of APIs with special focus on machine learning (ML).\nThe main aim of the framework is to make ridiculously simple the deployment of\nML APIs, simplifying (when possible) the entire process to a single line of\ncode.\n\nThe library builds on Starlette, and provides an easy-to-learn\nphilosophy to speed up the building of highly performant GraphQL, REST and ML APIs.\nBesides, it comprises an ideal solution for the development of asynchronous\nand production-ready services, offering automatic deployment for ML models.\n\nSome remarkable characteristics:\n\n* Generic classes for API resources with the convenience of standard CRUD methods over SQLAlchemy tables.\n* A schema system (based on Marshmallow or Typesystem) which allows the declaration of inputs and outputs of endpoints\n  very easily, with the convenience of reliable and automatic data-type validation.\n* Dependency injection to make ease the process of managing parameters needed in endpoints via the use of `Component`s.\n  Flama ASGI objects like `Request`, `Response`, `Session` and so on are defined as `Component`s ready to be injected in\n  your endpoints.\n* `Component`s as the base of the plugin ecosystem, allowing you to create custom or use those already defined in your\n  endpoints, injected as parameters.\n* Auto generated API schema using OpenAPI standard.\n* Auto generated `docs`, and provides a Swagger UI and ReDoc endpoints.\n* Automatic handling of pagination, with several methods at your disposal such as `limit-offset` and `page numbering`,\n  to name a few.\n\n## Installation\n\nFlama is fully compatible with all [supported versions](https://devguide.python.org/versions/) of Python. We recommend\nyou to use the latest version available.\n\nFor a detailed explanation on how to install flama\nvisit:  [https://flama.dev/docs/getting-started/installation](https://flama.dev/docs/getting-started/installation).\n\n## Getting Started\n\nVisit [https://flama.dev/docs/getting-started/quickstart](https://flama.dev/docs/getting-started/quickstart) to get\nstarted with Flama.\n\n## Documentation\n\nVisit [https://flama.dev/docs/](https://flama.dev/docs/) to view the full documentation.\n\n## Example\n\n```python\nfrom flama import Flama\n\napp = Flama(\n    title="Hello-🔥",\n    version="1.0",\n    description="My first API",\n)\n\n\n@app.route("/")\ndef home():\n    """\n    tags:\n        - Salute\n    summary:\n        Returns a warming message.\n    description:\n        This is a more detailed description of the method itself.\n        Here we can give all the details required and they will appear\n        automatically in the auto-generated docs.\n    responses:\n        200:\n            description: Warming hello message!\n    """\n    return {"message": "Hello 🔥"}\n```\n\nThis example will build and run a `Hello 🔥` API. To run it:\n\n```commandline\nflama run examples.hello_flama:app\n```\n\n## Authors\n\n* José Antonio Perdiguero López ([@perdy](https://github.com/perdy/))\n* Miguel Durán-Olivencia ([@migduroli](https://github.com/migduroli/))\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, please read\nour [contributing docs](.github/CONTRIBUTING.md) **before submitting** a pull\nrequest.\n',
    'author': 'José Antonio Perdiguero López',
    'author_email': 'perdy@perdy.io',
    'maintainer': 'José Antonio Perdiguero López',
    'maintainer_email': 'perdy@perdy.io',
    'url': 'https://flama.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
