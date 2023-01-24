# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['diffenator2']

package_data = \
{'': ['*'], 'diffenator2': ['data/*', 'data/wordlists/*', 'templates/*']}

install_requires = \
['Pillow',
 'blackrenderer[skia]>=0.6.0,<0.7.0',
 'fontTools[ufo]>=4.37.3',
 'freetype-py',
 'gflanguages',
 'jinja2',
 'ninja',
 'protobuf>=3.19.2,<=3.20.3',
 'pyahocorasick',
 'selenium>=4.4.3',
 'tqdm>=4.64.1,<5.0.0',
 'uharfbuzz',
 'unicodedata2>=15.0.0,<16.0.0',
 'youseedee>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['_diffbrowsers = diffenator2._diffbrowsers:main',
                     '_diffenator = diffenator2._diffenator:main',
                     'diffenator2 = diffenator2.__main__:main']}

setup_kwargs = {
    'name': 'diffenator2',
    'version': '0.0.4',
    'description': 'Compare two fonts',
    'long_description': 'None',
    'author': 'Marc Foley',
    'author_email': 'm.foley.88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
