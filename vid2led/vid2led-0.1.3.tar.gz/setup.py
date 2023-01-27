# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vid2led']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.7.0.68,<5.0.0.0']

extras_require = \
{':sys_platform == "linux"': ['rpi-ws281x>=4.3.4,<5.0.0'],
 ':sys_platform == "win32"': ['rpi-ws281x-mock>=0.2.2,<0.3.0']}

entry_points = \
{'console_scripts': ['vid2led = vid2led.cli:main']}

setup_kwargs = {
    'name': 'vid2led',
    'version': '0.1.3',
    'description': 'A command line tool to play videos on WS281x LED matrices',
    'long_description': '# vid2led\nTool to play videos on WS281x LED matrices.',
    'author': 'Will McGloughlin',
    'author_email': 'willem.mcg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
