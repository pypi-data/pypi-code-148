# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymage_size']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymage-size',
    'version': '1.7.1',
    'description': 'A Python package for getting the dimensions of an image without loading it into memory.',
    'long_description': '# pymage_size\n[![Downloads](https://pepy.tech/badge/pymage_size)](https://pepy.tech/project/pymage_size)\n\nA Python package for getting the dimensions of an image without loading it into memory. No external dependencies either!\n\n## Installation\npymage_size is available from PyPI, so you can install via `pip`:\n```bash\n$ pip install pymage_size\n```\n\n## Usage\n```python\nfrom pymage_size import get_image_size\n\nimg_format = get_image_size("example.png")\nwidth, height = img_format.get_dimensions()\n```\n',
    'author': 'cobaltcore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kobaltcore/pymage_size',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
