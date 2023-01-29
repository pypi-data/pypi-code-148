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
    'version': '0.2.2',
    'description': 'A package to generate color sequences from videos and images',
    'long_description': '# pyrolld\n\nA package to generate color sequences from videos and images\n\nIts main use is to create a set of unique colors from an image and then\nsort the colors according to the selected sorting method.\n\n## Installation\n\nYou can simply pip install this package:\n\n```bash\npip install pyrolld\n```\n\n## Usage\n\nHere is an example:\n\n```python\nfrom rolld import Roller\n\n\nfilepath = "image.png"\nimage = Roller(filepath)\nrolled = image.roll()\n\nrolled.show()\n```\n\nYou can also chose between 3 different sorting methods `["HSV", "HSL", "YIQ", "LUM"]`:\n\n```python\nfrom rolld import Roller\n\n\nfilepath = "image.png"\nimage = Roller(filepath)\nrolled = image.roll(sorter="LUM")\n\nrolled.show()\n```\n\n\n## Example\n\nHere is an example. We are going to use the image `lena.png`:\n\n<img src="https://raw.githubusercontent.com/Vitaman02/pyrolld/main/assets/images/lena.png" width="250" height="250">\n\nAnd with this code we will "roll" the image:\n\n```python\nfrom rolld import Roller\n\n\nfilepath = "lena.png"\nroller = Roller(filepath)\n\nsorters = ["HSV", "HSL", "YIQ", "LUM"]\nfor sorter in sorters:\n    image = roller.roll(sorter=sorter)\n    image.show()\n\n```\n\nHere is the output of all the sorting methods:\n\n### Luminance\n\n<img src="https://raw.githubusercontent.com/Vitaman02/pyrolld/main/assets/images/lena_lum.png">\n\n### YIQ\n\n<img src="https://raw.githubusercontent.com/Vitaman02/pyrolld/main/assets/images/lena_yiq.png">\n\n### HSV\n\n<img src="https://raw.githubusercontent.com/Vitaman02/pyrolld/main/assets/images/lena_hsv.png">\n\n### HSL\n\n<img src="https://raw.githubusercontent.com/Vitaman02/pyrolld/main/assets/images/lena_hsl.png">\n',
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
