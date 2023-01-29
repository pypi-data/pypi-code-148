# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jubeatools',
 'jubeatools.cli',
 'jubeatools.cli.tests',
 'jubeatools.cli.tests.data',
 'jubeatools.formats',
 'jubeatools.formats.jubeat_analyser',
 'jubeatools.formats.jubeat_analyser.memo',
 'jubeatools.formats.jubeat_analyser.memo1',
 'jubeatools.formats.jubeat_analyser.memo2',
 'jubeatools.formats.jubeat_analyser.mono_column',
 'jubeatools.formats.jubeat_analyser.tests',
 'jubeatools.formats.jubeat_analyser.tests.data',
 'jubeatools.formats.jubeat_analyser.tests.memo',
 'jubeatools.formats.jubeat_analyser.tests.memo1',
 'jubeatools.formats.jubeat_analyser.tests.memo2',
 'jubeatools.formats.jubeat_analyser.tests.mono_column',
 'jubeatools.formats.konami',
 'jubeatools.formats.konami.eve',
 'jubeatools.formats.konami.eve.tests',
 'jubeatools.formats.konami.eve.tests.data',
 'jubeatools.formats.konami.jbsq',
 'jubeatools.formats.konami.jbsq.tests',
 'jubeatools.formats.malody',
 'jubeatools.formats.malody.tests',
 'jubeatools.formats.malody.tests.data',
 'jubeatools.formats.memon',
 'jubeatools.formats.memon.v0',
 'jubeatools.formats.memon.v1',
 'jubeatools.formats.memon.v1.tests',
 'jubeatools.formats.tests',
 'jubeatools.testutils']

package_data = \
{'': ['*'], 'jubeatools.cli.tests.data': ['memon_merge/*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'construct-typing>=0.5.3,<0.6.0',
 'construct>=2.10,<3.0',
 'marshmallow-dataclass[union,enum]>=8.5.3,<9.0.0',
 'marshmallow>=3.6.0,<4.0.0',
 'more-itertools>=8.4.0,<9.0.0',
 'parsimonious>=0.10.0,<0.11.0',
 'python-constraint>=1.4.0,<2.0.0',
 'simplejson>=3.17.0,<4.0.0',
 'sortedcontainers>=2.3.0,<3.0.0',
 'typing-inspect==0.7.1']

entry_points = \
{'console_scripts': ['jubeatools = jubeatools.cli.cli:convert']}

setup_kwargs = {
    'name': 'jubeatools',
    'version': '2.0.6',
    'description': 'A toolbox for jubeat file formats',
    'long_description': '# Jubeatools\n\n[![docs status badge](https://readthedocs.org/projects/jubeatools/badge/)](https://jubeatools.readthedocs.io)\n\nA toolbox to convert between jubeat file formats\n\n## How to install\n```sh\npip install jubeatools\n```\n\nYou need Python 3.9 or greater\n\nMore details in [the documentation](https://jubeatools.readthedocs.io)\n\n## How to use in a command line\n```sh\njubeatools ${source} ${destination} -f ${output format} (... format specific options)\n```\n\nAgain, more details in [the documentation](https://jubeatools.readthedocs.io)\n\n## Which formats are supported\n|                 |                      | input | output |\n|-----------------|----------------------|:-----:|:------:|\n| memon           | v1.0.0               | ✔️     | ✔️      |\n|                 | v0.3.0               | ✔️     | ✔️      |\n|                 | v0.2.0               | ✔️     | ✔️      |\n|                 | v0.1.0               | ✔️     | ✔️      |\n|                 | legacy               | ✔️     | ✔️      |\n| jubeat analyser | #memo2               | ✔️     | ✔️      |\n|                 | #memo1               | ✔️     | ✔️      |\n|                 | #memo                | ✔️     | ✔️      |\n|                 | mono-column (1列形式) | ✔️     | ✔️      |\n| jubeat (arcade) | .eve                 | ✔️     | ✔️      |\n| jubeat plus     | .jbsq                | ✔️     | ✔️      |\n| malody          | .mc (Pad Mode)       | ✔️     | ✔️      |\n',
    'author': 'Stepland',
    'author_email': '10530295-Buggyroom@users.noreply.gitlab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/square-game-liberation-front/jubeatools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
