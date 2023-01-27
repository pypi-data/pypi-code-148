# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uploader', 'uploader.cleanup']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=4.2b1',
 'click>=7.0',
 'influx_line_protocol>=0.1.5',
 'minio>=4.0.17',
 'redis>=3.2.1',
 'requests>=2.28.1,<3.0.0',
 'wf-video-io>=3.2.1']

setup_kwargs = {
    'name': 'wf-classroom-video-uploader',
    'version': '1.0.11',
    'description': '',
    'long_description': '# TODO',
    'author': 'Paul J DeCoursey',
    'author_email': 'paul@decoursey.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
