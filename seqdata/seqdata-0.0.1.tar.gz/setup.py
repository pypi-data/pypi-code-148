# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqdata',
 'seqdata..ipynb_checkpoints',
 'seqdata._analyze',
 'seqdata._core',
 'seqdata._encode',
 'seqdata._io',
 'seqdata._preprocess']

package_data = \
{'': ['*']}

install_requires = \
['logomaker>=0.8,<0.9',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pybedtools>=0.9.0,<0.10.0',
 'pyranges>=0.0.117,<0.0.118',
 'seaborn>=0.11.2,<0.12.0']

extras_require = \
{':extra == "jaspar"': ['pyjaspar[jaspar]>=2.1.0,<3.0.0',
                        'biopython[jaspar]==1.77']}

setup_kwargs = {
    'name': 'seqdata',
    'version': '0.0.1',
    'description': 'Annotated sequence data',
    'long_description': '# SeqData\n',
    'author': 'Adam Klie',
    'author_email': 'aklie@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
