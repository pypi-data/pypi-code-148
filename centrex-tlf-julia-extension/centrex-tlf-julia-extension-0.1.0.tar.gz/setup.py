# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['centrex_tlf_julia_extension', 'centrex_tlf_julia_extension.lindblad_julia']

package_data = \
{'': ['*']}

install_requires = \
['centrex-tlf>=0.1.0,<0.2.0', 'julia>=0.6.0,<0.7.0', 'psutil>=5.9.4,<6.0.0']

setup_kwargs = {
    'name': 'centrex-tlf-julia-extension',
    'version': '0.1.0',
    'description': 'Extension for centrex-tlf to run OBE simulations in Julia',
    'long_description': '# CeNTREX-TlF-julia-extension\n Extension for centrex-tlf to run OBE simulations in Julia\n',
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ograsdijk/CeNTREX-TlF-julia-extension',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
