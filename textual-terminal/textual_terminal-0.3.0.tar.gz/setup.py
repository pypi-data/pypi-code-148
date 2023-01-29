# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_terminal']

package_data = \
{'': ['*']}

install_requires = \
['pyte>=0.8.1,<0.9.0', 'textual>=0.8.0']

setup_kwargs = {
    'name': 'textual-terminal',
    'version': '0.3.0',
    'description': 'A terminal emulator widget for Textual.',
    'long_description': '# Textual: Terminal\n\nA terminal widget for [Textual](https://github.com/Textualize/textual) using\n[Pyte](https://github.com/selectel/pyte) as a linux terminal emulator.\n\n<details><summary>Textual application example with two terminal widgets:</summary>\n\n![textual_terminal_example](https://user-images.githubusercontent.com/922559/214794889-4d376da1-6aa9-4576-a01d-0beee2536e41.png)\n\n</details>\n\n## Usage\n\n```python\nfrom textual_terminal import Terminal\n\nclass TerminalApp(App):\n    def compose(self) -> ComposeResult:\n        yield Terminal(command="htop", id="terminal_htop")\n        yield Terminal(command="bash", id="terminal_bash")\n\n    def on_ready(self) -> None:\n        terminal_htop: Terminal = self.query_one("#terminal_htop")\n        terminal_htop.start()\n\n        terminal_bash: Terminal = self.query_one("#terminal_bash")\n        terminal_bash.start()\n```\n\n## Installation\n\n```bash\npip install textual-terminal\n```\n\n## Features\n\n* Colored output\n* Automatic resize to widget dimensions\n* Simple key handling (navigation, function keys)\n* Simple mouse tracking (click, scroll)\n\n## Options\n\n### `default_colors`\n\nBy default, textual-terminal uses the colors defined by the system (not the\nTextual colors). To use the Textual background and foreground colors for\n"default" ANSI colors, set the option `default_colors` to `textual`:\n\n```python\nTerminal(command="htop", default_colors="textual")\n```\n\nNote: This only applies to ANSI colors without an explicit setting, e.g. if the\nbackground is set to "red" by an application, it will stay red and the option\nwill not have any effect.\n\n## References\n\nThis library is based on the\n[Textual pyte example](https://github.com/selectel/pyte/blob/master/examples/terminal_emulator.py)\nby [David Brochart](https://github.com/davidbrochart).\n',
    'author': 'Mischa Schindowski',
    'author_email': 'mschindowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mitosch/textual-terminal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
