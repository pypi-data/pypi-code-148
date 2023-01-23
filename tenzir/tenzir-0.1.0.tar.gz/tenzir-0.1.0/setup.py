# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tenzir']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tenzir',
    'version': '0.1.0',
    'description': 'Tenzir, Answer the toughest questions in cyber security',
    'long_description': '# Actionable Insights\n\n## Answer the toughest questions in cyber security\n\nOptimal posture for network-wide forensics\n\nData-driven protection for your network\n\nFaster threat detection & response\n\n<https://tenzir.com/>\n',
    'author': 'Tenzir',
    'author_email': 'engineering@tenzir.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
