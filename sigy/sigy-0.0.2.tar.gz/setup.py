# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sigy',
    'version': '0.0.2',
    'description': 'A library to enable reusing and composing Python function signatures.',
    'long_description': 'sigy\n_________________\n\n[![PyPI version](https://badge.fury.io/py/sigy.svg)](http://badge.fury.io/py/sigy)\n[![Test Status](https://github.com/timothycrosley/sigy/workflows/Test/badge.svg?branch=develop)](https://github.com/timothycrosley/sigy/actions?query=workflow%3ATest)\n[![Lint Status](https://github.com/timothycrosley/sigy/workflows/Lint/badge.svg?branch=develop)](https://github.com/timothycrosley/sigy/actions?query=workflow%3ALint)\n[![codecov](https://codecov.io/gh/timothycrosley/sigy/branch/main/graph/badge.svg)](https://codecov.io/gh/timothycrosley/sigy)\n[![Join the chat at https://gitter.im/timothycrosley/sigy](https://badges.gitter.im/timothycrosley/sigy.svg)](https://gitter.im/timothycrosley/sigy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/sigy/)\n[![Downloads](https://pepy.tech/badge/sigy)](https://pepy.tech/project/sigy)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/sigy/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/sigy/)\n_________________\n\n**sigy** A library to enable reusing and composing Python function signatures.\n',
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.7',
}


setup(**setup_kwargs)
