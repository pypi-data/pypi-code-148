# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts', 'quri_parts.openqasm', 'quri_parts.openqasm.circuit']

package_data = \
{'': ['*']}

install_requires = \
['quri-parts-circuit']

setup_kwargs = {
    'name': 'quri-parts-openqasm',
    'version': '0.5.0',
    'description': 'A support library for using OpenQASM 3 with QURI Parts',
    'long_description': '# QURI Parts OpenQASM\n\nQURI Parts OpenFermion is a support library for using OpenQASM 3 with QURI Parts.\n\nNote: some gates (SqrtX, SqrtXdag, SqrtY, SqrtYdag) are not implemented yet.\n\n## Documentation\n\n[QURI Parts Documentation](https://quri-parts.qunasys.com)\n\n## Installation\n\n```\npip install quri-parts-openqasm\n```\n\n## License\n\nApache License 2.0\n',
    'author': 'QURI Parts Authors',
    'author_email': 'opensource@qunasys.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/QunaSys/quri-parts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.8,<3.12',
}


setup(**setup_kwargs)
