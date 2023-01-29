# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eracore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eracore',
    'version': '0.0.6',
    'description': 'Core',
    'long_description': "# EraCore\n\nThis is a core for my package.\n\n##### CPF (Create project function):\n\n```\nfrom EraCore import ECore\n\nexample_variable = ECore()\nexample_variable.CPF(project_name='',\n                     project_version='',\n                     project_authors='',\n                     readme=True) # if readme = True, create readme file\n```\n\n##### CPI (Create project input):\n\n```\nfrom EraCore import ECore\n\nexample_variable = ECore()\nexample_variable.CPI() # Create project using input\n```\n\n##### R (Random):\n\n```\nfrom EraCore import ECore\n\nexample_variable = ECore()\nexample_variable.R()\n```\n",
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
