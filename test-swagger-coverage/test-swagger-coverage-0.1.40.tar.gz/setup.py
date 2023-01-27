# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swagger_coverage', 'swagger_coverage.scripts', 'swagger_coverage.src']

package_data = \
{'': ['*'], 'swagger_coverage.src': ['files/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'attrs>=21.4.0,<22.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['swagger_coverage = '
                     'swagger_coverage.scripts.swagger_report:main']}

setup_kwargs = {
    'name': 'test-swagger-coverage',
    'version': '0.1.40',
    'description': 'Swagger coverage for API tests',
    'long_description': '# swagger-coverage\n[![Tests](https://github.com/berpress/swagger-coverage/actions/workflows/python-app.yml/badge.svg)](https://github.com/berpress/swagger-coverage/actions/workflows/python-app.yml)\n![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)\n[![Maintainability](https://api.codeclimate.com/v1/badges/45afb8b947b1c7e9cec8/maintainability)](https://codeclimate.com/github/berpress/swagger-coverage/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/45afb8b947b1c7e9cec8/test_coverage)](https://codeclimate.com/github/berpress/swagger-coverage/test_coverage)\n[![PyPI version](https://badge.fury.io/py/test-swagger-coverage.svg)](https://badge.fury.io/py/test-swagger-coverage)\n[![Downloads](https://pepy.tech/badge/test-swagger-coverage)](https://pepy.tech/project/test-swagger-coverage)\n\nAbout\n------------\n\nSwagger coverage report helps the QA automation and developer to get a simple API coverage report for endpoints tests\n\n![](https://github.com/berpress/python-api-tests/blob/main/images/swagger_report_2.png)\n\nInstallation\n------------\n\nYou can install ``test-swagger-coverage`` via `pip`_ from `PyPI`_::\n\n    $ pip install test-swagger-coverage\n\nor with poetry\n\n    $ poetry add test-swagger-coverage\n\nHow it works\n------------\nWe take a swagger as data for testing coverage and, based on it, we create a file that will be the settings for our tests. The file can be created automatically or manually.\n\nNext, we set up api calls in our tests (we wrap them with decorators, see examples) and at the end of testing we generate html report.\nWe will check which endpoints were called and what statuses we checked.\n\nWe can\'t always trust our swagger, so you can manually set the status of the codes yourself, which need to be checked.\n\nExamples\n------------\n\nFirst, we need a link to your swagger. For example,  let\'s take this  https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0 (see more about this api https://github.com/berpress/flask-restful-api),\nand take url to yaml/yml/json swagger file - https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0\n\nNext, in our project, we need to create a file describing our endpoints, which our tests will use to generate a coverage report.\n\nWe can do it automatically via the command line\n\n    $ swagger_coverage https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0\n\nResult\n\n    $ 2022-04-15 11:22:37 INFO Start load swagger https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0\n    $ 2022-04-15 11:22:38 INFO The swagger report was successfully saved to the folder: /Users/user/Documents/git/python-api-tests/swagger_report\n\n\n\nThe **swagger_report** directory will be created\nand a **data_swagger.yaml** file will appear inside, which will be the settings for building a test coverage report\n\nThe **data_swagger.yaml** file looks something like this\n\n\n ```\n ...\nregUser:\n  description: null\n  method: POST\n  path: /register\n  statuses:\n  - 201  <---- change from 200 to 201\n  - 400\n  - 401\n  - 403\n  tag: register\n  ...\n ```\n\nwhere **regUser** is the unique id of our endpoint\n\n**statuses** is a list of statuses that we will check (that they were called).\nYou can customize this list yourself.\n\nOnly we will check 201 status, as described in the user registration swagger. So I will add it.\n\n\nLet\'s create a simple test and build a report. For requests, you will use the **requests** library.\n\n```python\nimport requests\nfrom swagger_coverage.src.coverage import SwaggerCoverage\nfrom swagger_coverage.src.deco import swagger\n\n# swagger data preparation\nswagger_url = "https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0"\napi_url = "https://api.swaggerhub.com/apis/"\npath=\'/report\' # path to swagger coverage report\nswagger_rep = SwaggerCoverage(api_url=api_url, url=swagger_url, path=path)\nswagger_rep.create_coverage_data()\n\n\n# function to call a request to the server\n@swagger("regUser")\ndef register_user(payload: dict):\n    return requests.post(\'https://stores-tests-api.herokuapp.com/register\',\n                         json=payload)\n\n\n# test\ndata = {"username": "test2023@test.com", "password": "Password"}\nresponse = register_user(data)\nassert response.status_code == 201\n\n# create report\nswagger_rep.create_report()\n\n```\n**swagger data preparation**: Prepare our file data_swagger.yaml, it will be created automatically.\n\n**function to call a request to the server**:  We will write a user registration call. Declaring a function with a decorator **@swagger("regUser")**.\n**"regUser"** taken from file **data_swagger.yaml**, this is unique id of our endpoint.\n\n**test**: run the test\n\n**create report**: create a report.\n\n\nAfter that, in the folder **swagger_report** we will receive a report **index.html**.\n\nLet\'s see it\n\n![](https://github.com/berpress/python-api-tests/blob/main/images/swagger_register.png)\n\nAs you can see, we have increased the counter of verified endpoints\n\nIf you use **pytest**, add this code in conftest.py\n\n```python\n@pytest.fixture(scope="session", autouse=True)\ndef swagger_checker(request):\n    url = request.config.getoption("--swagger-url")\n    url_api = request.config.getoption("--api-url")\n    path = \'/report\'\n    swagger = SwaggerCoverage(api_url=url_api, url=url, path=path)\n    swagger.create_coverage_data()\n    yield\n    swagger.create_report()\n```\n\nMore example with pytest and API tests https://github.com/berpress/python-api-tests\n\nReport example [https://github.com/berpress/python-api-tests/tree/main/swagger_report](https://github.com/berpress/python-api-tests/tree/main/report)\n',
    'author': 'alexanderlozovoy',
    'author_email': 'berpress@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/berpress/swagger-coverage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
