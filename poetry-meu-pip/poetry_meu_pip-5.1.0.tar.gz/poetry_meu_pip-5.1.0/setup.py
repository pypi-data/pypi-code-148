# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_base']

package_data = \
{'': ['*']}

install_requires = \
['altair==4.2.0']

setup_kwargs = {
    'name': 'poetry-meu-pip',
    'version': '5.1.0',
    'description': 'Projeto final da disciplina de gces - UnB',
    'long_description': '# Poetry do trabalho final de gces\n\n# Para instalar utilizar pip install poetry-tfs',
    'author': 'ArthurMeloG',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
