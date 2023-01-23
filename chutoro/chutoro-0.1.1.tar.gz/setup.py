# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chutoro']

package_data = \
{'': ['*']}

install_requires = \
['pymupdf>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'chutoro',
    'version': '0.1.1',
    'description': '',
    'long_description': '# chutoro\n\nHighlight sentences in PDF files using any sentence classification models.\n\n\n# Usage\n\n## Installation\n\n```bash\npip install chutoro\n```\n\n## Example\n\nCheckout `./examples/main.py`.\n',
    'author': 'sobamchan',
    'author_email': 'oh.sore.sore.soutarou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
