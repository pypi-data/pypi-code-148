# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loapy', 'loapy.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'ujson>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'loapy',
    'version': '0.0.2',
    'description': 'An unofficial asynchronous SDK for Lostark Open API written in Python.',
    'long_description': '# loapy\n\nAn unofficial asynchronous SDK for Lostark Open API written in Python.\n\n## Installation\n\n**loapy requires Python 3.7 or higher**\n\n```sh\npython -m pip install --upgrade loapy\n```\n\n## Usage\n\n```python\nfrom asyncio import run\nfrom loapy import LostArkRest\n\nlostark = LostArkRest("your_api_key_here")\n\nasync def main() -> None:\n    print(\n        await lostark.fetch_events()\n    )\n\nrun(main())\n```',
    'author': 'Mary',
    'author_email': 'mareowst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
