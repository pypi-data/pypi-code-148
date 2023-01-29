# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rolld']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.0,<10.0', 'types-pillow>=9.0,<10.0']

setup_kwargs = {
    'name': 'pyrolld',
    'version': '0.1.1',
    'description': 'A package to generate color sequences from videos and images',
    'long_description': '# pyrolld\n\nA package to generate color sequences from videos and images\n\nIts main use is to create a set of unique colors from an image and then\nsort the colors according to the selected sorting method.\n\n# Installation\n\nYou can simply pip install this package:\n\n```bash\npip install pyrolld\n```\n\n# Usage\n\nHere is an example:\n\n```python\nfrom rolld import Roller\n\n\nfilepath = "image.png"\nimage = Roller(filepath)\nrolled = image.roll()\n\nrolled.show()\n```\n\nYou can also chose between 3 different sorting methods `["HSV", "HSL", "LUM"]`:\n\n```python\nfrom rolld import Roller\n\n\nfilepath = "image.png"\nimage = Roller(filepath)\nrolled = image.roll(sorter="LUM")\n\nrolled.show()\n```\n',
    'author': 'Vitaman02',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
