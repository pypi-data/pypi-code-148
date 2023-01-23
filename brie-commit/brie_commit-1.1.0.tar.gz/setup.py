# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brie_commit']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['good2gouda = brie_commit.gouda:main']}

setup_kwargs = {
    'name': 'brie-commit',
    'version': '1.1.0',
    'description': 'A collection of cheesy pre-commit hooks.',
    'long_description': "# brie-commit\nA collection of cheesy [pre-commit](https://pre-commit.com/) hooks\n\n## Using brie-commit with pre-commit\nAdd this to your `.pre-commit-config.yaml`\n\n```yaml\nrepos:\n-   repo: https://github.com/sco1/brie-commit\n    rev: v1.1.0\n    hooks:\n    -   id: brie-commit\n```\n\n## Hooks\n### `brie-commit`\nThis hook doesn't do anything except add cheese to your pre-commit invocation.\n\n```bash\n$ pre-commit run\n🧀🧀🧀...................................................................Passed\n```\n\n### `up-to-no-gouda`\nThis hook replaces all instances of `good` with `gouda` in your text files.\n",
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
