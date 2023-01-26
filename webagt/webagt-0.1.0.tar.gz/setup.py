# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['webagt']
install_requires = \
['certifi>=2022.9.14,<2023.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'easyuri>=0.0.12',
 'httpagentparser>=1.9.1,<2.0.0',
 'lxml>=4.9.1,<5.0.0',
 'microformats>=0.0.24',
 'mimeparse>=0.1.3,<0.2.0',
 'pendulum>=2.1.2,<3.0.0',
 'pyscreenshot>=3.0,<4.0',
 'pyvirtualdisplay>=3.0,<4.0',
 'requests[socks]>=2.27.1,<3.0.0',
 'selenium>=4.1.2,<5.0.0',
 'sqlyte>=0.0.50',
 'txtint>=0.0.68',
 'webdriver-manager>=3.8.1,<4.0.0']

entry_points = \
{'console_scripts': ['webcli = web.__main__:main']}

setup_kwargs = {
    'name': 'webagt',
    'version': '0.1.0',
    'description': 'a web agent',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/webagt',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
