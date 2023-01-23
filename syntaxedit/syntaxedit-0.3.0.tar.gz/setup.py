# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syntaxedit']

package_data = \
{'': ['*']}

install_requires = \
['pygments>=2.14.0,<3.0.0', 'qtpy>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'syntaxedit',
    'version': '0.3.0',
    'description': 'Syntax highlighting Qt text widget',
    'long_description': '# syntaxedit\n\n[![test](https://github.com/davidwinter/syntaxedit/workflows/ci_cd/badge.svg)](https://github.com/davidwinter/syntaxedit/actions?query=workflow%3Aci_cd) [![PyPI](https://img.shields.io/pypi/v/syntaxedit)](https://pypi.org/project/syntaxedit/)\n\n> A simple Python Qt syntax highlighting widget\n\n![syntaxedit](https://raw.githubusercontent.com/davidwinter/syntaxedit/main/example.png)\n\n## Features\n\n- Extensive [syntax](https://pygments.org/languages/) and [theme](https://pygments.org/styles/) support - powered by [Pygments](https://pygments.org)\n- Set font and font size\n- Set indentation size\n\n## Usage\n\n1. Install package\n\n   ```shell\n   pip install syntaxedit\n   ```\n\n   Or\n\n   ```shell\n   poetry add syntaxedit\n   ```\n\n2. In your app, include the package, and create a `SyntaxEdit` widget:\n\n    ```python\n    from syntaxedit.core import SyntaxEdit\n\n    code = """# Todo list\n\n    - [ ] Go shopping\n    - [x] Walk the dog"""\n\n    widget = SyntaxEdit(code)\n    ```\n\n### Available options\n\n- `content`: the initial content for the widget. **Default:** `""`\n- `parent`: parent Qt widget for SyntaxEdit. **Default:** `None`\n- `font`: the font family for the widget. **Default:** `"Courier New"`\n- `font_size`: size to use for the font. **Default:** `13`\n- `syntax`: the code [syntax](https://pygments.org/languages/) to use. **Default:** `"Markdown"`\n- `theme`: the syntax [theme](https://pygments.org/styles/) to use. **Default:** `"solarized-light"`\n- `indentation_size`: the size for indentation. **Default:** `4`\n- `use_theme_background`: whether to use the background colour from the theme or to not set one. **Default:** `True`\n\n## Authors\n\nBy [David Winter](https://github.com/davidwinter)\n\n## License\n\nMIT\n',
    'author': 'David Winter',
    'author_email': 'i@djw.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidwinter/syntaxedit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
