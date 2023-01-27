# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['anton']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'anton',
    'version': '0.1.0',
    'description': '',
    'long_description': '<div align="center">\n\n# anton\n\n[![CI testing](https://github.com/karthikrangasai/anton/actions/workflows/ci-testing.yml/badge.svg)](https://github.com/karthikrangasai/anton/actions/workflows/ci-testing.yml)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![Documentation Status](https://readthedocs.org/projects/anton/badge/?version=latest)](https://anton.readthedocs.io/en/latest/?badge=latest)\n\n<!-- [![PyPI](https://img.shields.io/pypi/v/anton)](Add PyPI Link here) -->\n<!-- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/karthikrangasai/anton/blob/master/training_notebook.ipynb) -->\n\n</div>\n\n`anton` is a Python library for auto instantiating yaml definitions to user defined dataclasses.\n\nAvoid boilerplate and get runtime type checking before the objects are created.\n\n<!-- ## Installation\n\n```bash\npip install anton\n``` -->\n\n## Usage\n\nGiven a `yaml` file definition in a file `index.yaml` as follows:\n\n```yaml\n# index.yaml\ninteger: 23\nstring: "Hello world"\npoint:\n  x: 0\n  y: 0\nline_segment:\n  first_point:\n    x: 10\n    y: 10\n  second_point:\n    x: 10\n    y: 10\n```\n\n`yaml_conf` lets you avoid writing the biolerplate code for loading the `yaml` file and parsing the python dictionary to instantiate the Dataclass object as follows:\n\n```py\n>>> from dataclasses import dataclass\n>>> from anton import yaml_conf\n>>>\n>>> @dataclass\n... class Point:\n...     x: int\n...     y: int\n...\n>>> @dataclass\n... class LineSegment:\n...     first_point: Point\n...     second_point: Point\n...\n>>> @yaml_conf(conf_path="index.yaml")\n... class ExampleClass:\n...     integer: int\n...     string: str\n...     point: Point\n...     line_segment: LineSegment\n...\n>>> example_obj = ExampleClass()\n>>> example_obj\nExampleClass(integer=23, string=\'Hello world\', point=Point(x=0, y=0), line_segment=LineSegment(first_point=Point(x=10, y=10), second_point=Point(x=10, y=10)))\n```\n\n## Roadmap\n\nCurrently the project only supports Python3.8\n\nRuntime type checking is supported for the following types:\n- int\n- float\n- str\n- bool\n- typing.List\n- typing.Dict\n- typing.Union\n- Any user defined dataclass\n\nThe ultimate aim is to support all python versions Python3.8+ and all possible type combinations.\n\n## Contributing\n\nPull requests are welcome !!! Please make sure to update tests as appropriate.\n\nFor major changes, please open an issue first to discuss what you would like to change.\n\nPlease do go through the [Contributing Guide](https://github.com/karthikrangasai/anton/blob/master/CONTRIBUTING.md) if some help is required.\n\nNote: `anton` currently in active development. Please [open an issue](https://github.com/karthikrangasai/anton/issues/new/choose) if you find anything that isn\'t working as expected.\n',
    'author': 'Karthik Rangasai Sivaraman',
    'author_email': 'karthikrangasai@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/karthikrangasai/anton',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
