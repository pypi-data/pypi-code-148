# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['netrics',
 'netrics.measurement',
 'netrics.measurement.builtin',
 'netrics.measurement.common',
 'netrics.measurement.common.connectivity',
 'netrics.task']

package_data = \
{'': ['*'], 'netrics': ['cli/include/banner/*', 'conf/include/*']}

install_requires = \
['fate-scheduler==0.1.0-rc.4', 'netifaces>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['netrics = netrics:main',
                     'netrics-dev = netrics.measurement.dev:main',
                     'netrics-dns-latency = '
                     'netrics.measurement.dns_latency:main',
                     'netrics-ndt7 = netrics.measurement.ndt7:main',
                     'netrics-ookla = netrics.measurement.ookla:main',
                     'netrics-ping = netrics.measurement.ping:main',
                     'netrics-traceroute = netrics.measurement.traceroute:main',
                     'netrics.d = netrics:daemon',
                     'netrics.s = netrics:serve']}

setup_kwargs = {
    'name': 'netrics-measurements',
    'version': '0.0.1rc1',
    'description': 'The extensible network measurements framework',
    'long_description': 'None',
    'author': 'Jesse London',
    'author_email': 'jesselondon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
