# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['top',
 'top.core',
 'top.gunicorn',
 'top.redis',
 'top.restapi',
 'top.tui',
 'top.web']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'emoji-country-flag>=1.3.1,<2.0.0',
 'iso8601>=1.0.2,<2.0.0',
 'redispy>=3.0.0,<4.0.0',
 'textual>=0.1.18,<0.2.0',
 'typer>=0.6.1,<0.7.0']

extras_require = \
{'docs': ['sphinx-sitemap>=2.2.0,<3.0.0',
          'Sphinx>=5.1.1,<6.0.0',
          'furo>=2022.6.21,<2023.0.0',
          'sphinx-autodoc-typehints>=1.16.0,<2.0.0'],
 'gunicorn': ['gunicorn>=20.1.0,<21.0.0', 'python-lorem>=1.1.2,<2.0.0']}

entry_points = \
{'console_scripts': ['random-http-requests = top.web.random_requests:main',
                     'web-top = top.web.main:app']}

setup_kwargs = {
    'name': 'top-framework',
    'version': '0.3.2',
    'description': 'Python framework for creating UNIX top like TUI applications easily',
    'long_description': "[![Automated test suite](https://github.com/tradingstrategy-ai/top-framework/actions/workflows/test.yml/badge.svg)](https://github.com/tradingstrategy-ai/top-framework/actions/workflows/test.yml)\n\n[![Documentation Status](https://readthedocs.org/projects/top-framework/badge/?version=latest)](https://top-framework.readthedocs.io/en/latest/?badge=latest)\n\nTop Framework is a Python library for writing UNIX top like Text User Interface applications.\n\nIt comes with [web-top](https://github.com/tradingstrategy-ai/web-top),\na`top` like monitoring tool for HTTP requests and responses on any web server.\n\n![screenshot](https://raw.githubusercontent.com/tradingstrategy-ai/top-framework/master/docs/source/web-top/screenshot2.png)\n\n# Use cases\n\nThe goal of Top Framework is to make is easy to roll out \ncustom live monitoring tools with text user interface quickly.\nSometimes you just need to log in to your server and see what's going on.\nTop tools are is ideal for observing and catching issues when they happen.\nThese tools are supplement for Application Performance Management (APM),\nmetrics like statsd and Prometheus and logging.\n\nMonitoring use cases you might have include:\n\n- HTTP request/response trackers for web servers\n\n- Background job trackers for Cron, Celery and other background job managers\n\n# Documentation\n\n- [Browse documentation](https://top-framework.readthedocs.io/)\n\n# Community \n\n- [Join Discord for any questions](https://tradingstrategy.ai/community)\n\n# Social media\n\n- [Follow on Twitter](https://twitter.com/TradingProtocol)\n- [Follow on Telegram](https://t.me/trading_protocol)\n- [Follow on LinkedIn](https://www.linkedin.com/company/trading-strategy/)\n\n# License\n\nMIT.\n\n[Developed and maintained by Trading Strategy](https://tradingstrategy.ai).",
    'author': 'Mikko Ohtamaa',
    'author_email': 'mikko@opensourcehacker.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tradingstrategy-ai/top-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
