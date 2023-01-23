# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apispec_ui']

package_data = \
{'': ['*'], 'apispec_ui': ['swagger-ui/*']}

install_requires = \
['environs>=9.5.0,<10.0.0', 'gunicorn>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'apispec-ui',
    'version': '0.1.4',
    'description': "Generate UI interactive API's from APISpec specifications.",
    'long_description': '**********\napispec-ui\n**********\n\n.. image:: https://img.shields.io/pypi/v/apispec-ui\n    :target: https://pypi.org/project/apispec-ui\n    :alt: PyPI version\n.. image:: https://github.com/codectl/apispec-ui/actions/workflows/ci.yaml/badge.svg\n    :target: https://github.com/codectl/apispec-ui/actions/workflows/ci.yaml\n    :alt: CI\n.. image:: https://codecov.io/gh/codectl/apispec-ui/branch/master/graph/badge.svg\n    :target: https://app.codecov.io/gh/codectl/apispec-ui/branch/master\n    :alt: codecov\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: code style: black\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: license: MIT\n\nA library to generate a UI interface from an `APISpec <https://github\n.com/marshmallow-code/apispec>`__ specification. As per the APISpec initiative, it\ncurrently supports `OpenAPI Specification <https://github\n.com/OAI/OpenAPI-Specification>`__ (aka. Swagger specification) and `SwaggerUI\n<https://swagger.io/tools/swagger-ui/>`__.\n\nFeatures\n========\n* Supports the OpenAPI Specification (versions 2 and 3)\n* Supports SwaggerUI for Swagger specifications (latest version - 4.0.0)\n* Currently supported frameworks include:\n\n  * Flask\n\n\nInstallation\n============\nInstall the package directly from ``PyPI`` (recommended):\n\n.. code-block:: bash\n\n    $ pip install -U apispec-ui\n\n\nPlugin dependencies like ``apispec`` and ``Flask`` are not installed with the package\nby default. To have it installed, do like so:\n\n.. code-block:: bash\n\n    $ pip install -U apispec-ui[apispec,Flask]\n\nExample usage\n=============\nA simple example on how to work with a ``Flask`` application:\n\n.. code-block:: python\n\n    from apispec import APISpec\n    from apispec.ext.marshmallow import MarshmallowPlugin\n    from apispec_plugins import FlaskPlugin\n    from apispec_ui.flask import Swagger\n    from flask import Flask\n\n    app = Flask(__name__)\n    apispec = APISpec(\n        title="Test API",\n        version="0.1.0",\n        openapi_version="3.0.3",\n        plugins=(FlaskPlugin(), MarshmallowPlugin()),  # optional\n    )\n    ...\n    Swagger(app=app, apispec=apispec, config={})\n\nWith this example, the application contains 2 extra views:\n\n- ``swagger.ui``: endpoint to serve ``SwaggerUI``\n- ``swagger.specs``: endpoint to serve ``swagger`` specs, in ``yaml``\n\nWith ``configs`` parameter one can tweak some parameters:\n\n.. code-block:: python\n\n    config = {\n        "swaggerui": True,  # enable/disable SwaggerUI\n        "swagger_route": "/api/",  # change swagger routes\n        "swagger_static": "/static/",  # change location for static files\n        "swagger_favicon": "favicon.ico",  # change favicon\n        "swagger_hide_bar": True,  # hide SwaggerUI top bar\n    }\n\nThese settings can also be configured through the ``SWAGGER`` config variable that is\npart of the app config.\n\nIn terms of precedence, the config that takes the most precedence is the ``config``\nparameter from ``Swagger`` class, followed by the ``SWAGGER`` app config.\n\nTests & linting 🚥\n==================\nRun tests with ``tox``:\n\n.. code-block:: bash\n\n    # ensure tox is installed\n    $ tox\n\nRun linter only:\n\n.. code-block:: bash\n\n    $ tox -e lint\n\nOptionally, run coverage as well with:\n\n.. code-block:: bash\n\n    $ tox -e coverage\n\nLicense\n=======\nMIT licensed. See `LICENSE <LICENSE>`__.\n',
    'author': 'Renato Damas',
    'author_email': 'rena2damas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/codectl/apispec-ui',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
