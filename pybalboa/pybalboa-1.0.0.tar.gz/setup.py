# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybalboa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybalboa',
    'version': '1.0.0',
    'description': 'Module to communicate with a Balboa spa wifi adapter.',
    'long_description': 'pybalboa\n--------\n\nPython Module to interface with a balboa spa\n\nRequires Python 3 with asyncio.\n\nTo Install::\n\n  pip install pybalboa\n\nTo test::\n\n  python3 pybalboa <ip-of-spa-wifi> <debug-flag>\n\nTo Use\n``````\n\nSee ``__main__.py`` for usage examples.\n\nMinimal example::\n\n  import asyncio\n  import pybalboa\n\n  async with pybalboa.SpaClient(spa_host) as spa:\n    # read/run spa commands\n  return\n\n\nRelated\n```````\n- https://github.com/ccutrer/balboa_worldwide_app/wiki - invaluable wiki for Balboa module protocol\n',
    'author': 'Nathan Spencer',
    'author_email': 'natekspencer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/garbled1/pybalboa',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
