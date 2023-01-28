# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eracore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eracore',
    'version': '0.0.4',
    'description': 'Core',
    'long_description': '# EraCore\n\n### This is a core for my package\n\n##### CP (Create project):\n\n```\nfrom EraCore import ECore\n\nexample_variable = ECore()\nexample_variable.CP() # arguments\n```\n',
    'author': 'Eragod',
    'author_email': 'eragod1337@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
