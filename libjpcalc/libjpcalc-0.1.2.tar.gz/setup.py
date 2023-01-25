# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libjpcalc', 'libjpcalc.soma', 'libjpcalc.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['somar = libjpcalc.soma:somar_cli']}

setup_kwargs = {
    'name': 'libjpcalc',
    'version': '0.1.2',
    'description': 'Exemplo de bibliotecas para ser utilizada',
    'long_description': '',
    'author': 'Julio Pereira',
    'author_email': 'juliocezar.marketing@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
