# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mplscience', 'mplscience._styledata']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'seaborn']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'mplscience',
    'version': '0.0.6',
    'description': 'Matplotlib style for scientific publications.',
    'long_description': '# mplscience\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11ZA7lq-nFpNpFFWqXnlCphRR6_N9qXP3?usp=sharing)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nMatplotlib style for scientific publications. This style keeps things pretty simple and aims to make moderate improvements to the base matplotlib style. It also sets things like the PDF font type to make it easier to interact with figures in Adobe Illustrator. Open the tutorial in Colab to see examples. `mplscience` is compatible with all Matplotlib-based packages, including Seaborn.\n\n## Usage\n\nTo install:\n\n```python\npip install mplscience\n```\n\nTo use:\n\n```python\nimport mplscience\nimport seaborn as sns\nmplscience.available_styles()\nmplscience.set_style()\ndf = sns.load_dataset("anscombe")\nsns.scatterplot(x="x", y="y", hue="dataset", data=df)\n```\n<img src="https://github.com/adamgayoso/mplscience/blob/main/images/scatter.png?raw=true" width="300" alt="scatter">\n\nIf you\'re using Seaborn, you may want to run `sns.reset_orig()` first to clear Seaborn-specific styling. You can also use the `reset_current` parameter of `mplscience` functions to reset any custom styling like this:\n\n```python\nmplscience.set_style(reset_current=True)\n```\n\n\nThe style can also be using in a context like this:\n\n```python\nimport mplscience\nwith mplscience.style_context():\n    plt.plot(x, y)\n```\n\n\n\n',
    'author': 'Adam Gayoso',
    'author_email': 'adamgayoso@berkeley.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adamgayoso/mplscience',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
