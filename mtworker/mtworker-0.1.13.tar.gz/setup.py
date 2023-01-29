# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtlibs',
 'mtlibs.mtlibs2',
 'mtlibs.mtlibs2.aws',
 'mtlibs.mtlibs2.cli',
 'mtlibs.mtlibs2.cli.sub_commands',
 'mtlibs.mtlibs2.data.openvpn',
 'mtlibs.mtlibs2.service',
 'mtlibs.tests',
 'mtlibs.tool',
 'mtworker',
 'mtworker.cmds',
 'mtworker.tasks',
 'mtworker.tasks.scrapy_tutorial',
 'mtworker.tasks.scrapy_tutorial.spiders']

package_data = \
{'': ['*'],
 'mtlibs': ['bin/*'],
 'mtlibs.mtlibs2': ['az/*',
                    'data/*',
                    'data/clash/*',
                    'data/mitmproxy/*',
                    'data/mtmitm/*',
                    'data/nginx/*',
                    'data/nginx/conf.d/*',
                    'data/tor/*',
                    'installers/*'],
 'mtlibs.mtlibs2.data.openvpn': ['ccd/*',
                                 'ovpn/*',
                                 'pki/*',
                                 'pki/certs_by_serial/*',
                                 'pki/issued/*',
                                 'pki/private/*',
                                 'pki/reqs/*',
                                 'pki/revoked/certs_by_serial/*',
                                 'pki/revoked/private_by_serial/*',
                                 'pki/revoked/reqs_by_serial/*']}

install_requires = \
['celery[redis]>=5.2.7,<6.0.0',
 'httpx>=0.23.3,<0.24.0',
 'playwright>=1.29.1,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'mtworker',
    'version': '0.1.13',
    'description': '',
    'long_description': 'None',
    'author': 'a',
    'author_email': 'a@a.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
