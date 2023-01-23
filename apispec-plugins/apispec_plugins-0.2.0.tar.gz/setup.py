# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apispec_plugins', 'apispec_plugins.webframeworks']

package_data = \
{'': ['*']}

install_requires = \
['apispec[yaml]>=6.0.1,<7.0.0']

extras_require = \
{'flask': ['Flask>=2.1.3,<3.0.0']}

setup_kwargs = {
    'name': 'apispec-plugins',
    'version': '0.2.0',
    'description': 'Plugins for apispec',
    'long_description': '***************\napispec-plugins\n***************\n\n.. image:: https://img.shields.io/pypi/v/apispec-plugins\n    :target: https://pypi.org/project/apispec-plugins\n    :alt: PyPI version\n.. image:: https://github.com/codectl/apispec-plugins/actions/workflows/ci.yaml/badge.svg\n    :target: https://github.com/codectl/apispec-plugins/actions/workflows/ci.yaml\n    :alt: CI\n.. image:: https://codecov.io/gh/codectl/apispec-plugins/branch/master/graph/badge.svg\n    :target: https://app.codecov.io/gh/codectl/apispec-plugins/branch/master\n    :alt: codecov\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: code style: black\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: license: MIT\n\n`APISpec <https://github.com/marshmallow-code/apispec>`__ plugins for easy\nintegration with different components (web frameworks, packages, etc).\n\nFeatures\n========\n* Supports the OpenAPI Specification (versions 2 and 3)\n* Currently supported frameworks/plugins include:\n\n  * ``apispec_plugins.webframeworks.flask``\n\nInstallation\n============\nInstall the package directly from ``PyPI`` (recommended):\n\n.. code-block:: bash\n\n   $ pip install apispec-plugins\n\nPlugin dependencies like ``Flask`` are not installed with the package by default. To\nhave ``Flask`` installed, do like so:\n\n.. code-block:: bash\n\n   $ pip install apispec-plugins[flask]\n\nExample Usage\n=============\n.. code-block:: python\n\n   from apispec import APISpec\n   from apispec_plugins.webframeworks.flask import FlaskPlugin\n   from flask import Flask\n\n   spec = APISpec(\n       title="Pet Store",\n       version="1.0.0",\n       openapi_version="2.0",\n       info=dict(description="A minimal pet store API"),\n       plugins=(FlaskPlugin(),),\n   )\n\n   app = Flask(__name__)\n\n\n   @app.route("/pet/<petId>")\n   def pet(petId):\n       """Find pet by ID.\n       ---\n       get:\n           parameters:\n               - in: path\n                 name: petId\n           responses:\n               200:\n                   description: display pet data\n       """\n       return f"Display pet with ID {petId}"\n\n\n   # Since `path` inspects the view and its route,\n   # we need to be in a Flask request context\n   with app.test_request_context():\n       spec.path(view=pet)\n\nAlternatively, a ``Flask`` ``MethodView`` can be used:\n\n.. code-block:: python\n\n   from flask.views import MethodView\n\n\n   class PetAPI(MethodView):\n       def get(self, petId):\n           # get pet by ID\n           pass\n\n\n   app.add_url_rule("/pet/<petId>", view_func=PetAPI.as_view("pet_view"))\n\nThere is also easy integration with other packages like\n``Flask-RESTful``:\n\n.. code-block:: python\n\n   from flask_restful import Api, Resource\n\n\n   class PetAPI(Resource):\n       def get(self, petId):\n           # get pet by ID\n           pass\n\n\n   api = Api(app)\n   api.add_resource(PetAPI, "/pet/<petId>", endpoint="pet")\n\nDynamic specs\n-------------\nAs seen so far, specs are specified in the docstring of the view or\nclass. However, with the ``spec_from`` decorator, one can dynamically\nset specs:\n\n.. code-block:: python\n\n   from apispec_plugins import spec_from\n\n\n   @spec_from(\n       {\n           "parameters": {"in": "path", "name": "petId"},\n           "responses": {200: {"description": "display pet data"}},\n       }\n   )\n   def pet(petID):\n       """Find pet by ID."""\n       pass\n\nWhy not ``apispec-webframeworks``?\n==================================\nThe conceiving of this project was based on `apispec-webframeworks <https://github\n.com/marshmallow-code/apispec-webframeworks>`__. While that project is focused on\nintegrating web frameworks with ``APISpec``, this repository goes a step further in\nproviding the best integration possible with the ``APISpec`` standards. Some\nlimitations on that project were also addressed, like:\n\n* a path cannot register no more than 1 single rule per endpoint;\n* support for additional libraries like ``Flask-RESTful``;\n* limited docstring spec processing;\n\nTests & linting 🚥\n==================\nRun tests with ``tox``:\n\n.. code-block:: bash\n\n    # ensure tox is installed\n    $ tox\n\nRun linter only:\n\n.. code-block:: bash\n\n    $ tox -e lint\n\nOptionally, run coverage as well with:\n\n.. code-block:: bash\n\n    $ tox -e coverage\n\nLicense\n=======\nMIT licensed. See `LICENSE <LICENSE>`__.\n',
    'author': 'Renato Damas',
    'author_email': 'rena2damas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/codectl/apispec-plugins',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
