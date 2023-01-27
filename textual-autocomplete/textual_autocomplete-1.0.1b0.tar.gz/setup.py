# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_autocomplete']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'textual-autocomplete',
    'version': '1.0.1b0',
    'description': 'Easily add autocomplete dropdowns to your Textual apps.',
    'long_description': '# textual-autocomplete\n\ntextual-autocomplete is a Python library for creating dropdown autocompletion menus in\nTextual applications, allowing users to quickly select from a list of suggestions as\nthey type.\n\n<img width="554" alt="image" src="https://user-images.githubusercontent.com/5740731/205718538-5599a9db-48a2-49dd-99c3-34d43459b81a.png">\n\n<details>\n<summary>Video example</summary>\n\nhttps://user-images.githubusercontent.com/5740731/205718330-a9364894-9133-40ca-8249-6e3dcc13f456.mov\n\n</details>\n\n## Quickstart\n\nSimply wrap a Textual `Input` widget as follows:\n\n```python\nfrom textual.app import ComposeResult\nfrom textual.widgets import Input\nfrom textual_autocomplete import AutoComplete, Dropdown, DropdownItem\n\ndef compose(self) -> ComposeResult:\n    yield AutoComplete(\n        Input(placeholder="Type to search..."),\n        Dropdown(items=[\n            DropdownItem("Glasgow"),\n            DropdownItem("Edinburgh"),\n            DropdownItem("Aberdeen"),\n            DropdownItem("Dundee"),\n        ]),\n    )\n```\n\nThere are more complete examples [here](./examples).\n\n## Installation\n\n`textual-autocomplete` can be installed from PyPI using your favourite dependency\nmanager.\n\n## Usage\n\n### Wrapping your `Input`\n\nAs shown in the quickstart, you can wrap the Textual builtin `Input` widget with\n`AutoComplete`, and supply a `Dropdown`. \nThe `AutoComplete` manages communication between the `Input` and the `Dropdown`.\n\nThe `Dropdown` is the widget you see on screen, as you type into the input.\n\nThe `DropdownItem`s contain up to 3 columns. All must contain a "main" column, which\nis the central column used in the filtering. They can also optionally contain a left and right metadata\ncolumn.\n\n### Supplying data to `Dropdown`\n\nYou can supply the data for the dropdown via a list or a callback function.\n\n#### Using a list\n\nThe easiest way to use textual-autocomplete is to pass in a list of `DropdownItem`s, \nas shown in the quickstart.\n\n#### Using a callable\n\nInstead of passing a list of `DropdownItems`, you can supply a callback function\nwhich will be called with the current value and cursor position in the input.\n\nSee [here](./examples/custom_meta.py) for a usage example.\n\n### Keyboard control\n\n- Press the Up/Down arrow keys to navigate.\n- Press Enter to select the item in the dropdown and fill it in.\n- Press Tab to fill in the selected item, and move focus.\n- Press Esc to hide the dropdown.\n- Press the Up/Down arrow keys to force the dropdown to appear.\n\n### Styling\n\nThe `Dropdown` itself can be styled using Textual CSS.\n\nFor more fine-grained control over styling, you can target the following CSS classes:\n\n- `.autocomplete--highlight-match`: the highlighted portion of a matching item\n- `.autocomplete--selection-cursor`: the item the selection cursor is on\n- `.autocomplete--left-column`: the left metadata column, if it exists\n- `.autocomplete--right-column`: the right metadata column, if it exists\n\nSince the 3 columns in `DropdownItem` support Rich `Text` objects, they can be styled dynamically.\nThe [custom_meta.py](./examples/custom_meta.py) file is an example of this, showing how the rightmost column is coloured dynamically based on the city population.\n\nThe [examples directory](./examples) contains multiple examples of custom styling.\n\n### Messages\n\nWhen you select an item in the dropdown, a `Dropdown.Selected` event is emitted.\n\nYou can declare a handler for this event `on_dropdown_selected(self, event)` to respond\nto an item being selected.\n\nAn item is selected when it\'s highlighted in the dropdown, and you press Enter or Tab.\n\nPressing Enter simply fills the value in the dropdown, whilst Tab fills the value\nand then shifts focus from the input.\n\n## Other notes\n\n- textual-autocomplete will create a new layer at runtime on the `Screen` that the `AutoComplete` is on. The `Dropdown` will be rendered on this layer.\n- The position of the dropdown is currently fixed _below_ the value entered into the `Input`. This means if your `Input` is at the bottom of the screen, it\'s probably not going to be much use for now. I\'m happy to discuss or look at PRs that offer a flag for having it float above.\n- There\'s currently no special handling for when the dropdown meets the right-hand side of the screen.\n- Do not apply `margin` to the `Dropdown`. The position of the dropdown is updated by applying margin to the top/left of it.\n- There\'s currently no debouncing support, but I\'m happy to discuss or look at PRs for this.\n- There are a few known issues/TODOs in the code, which will later be transferred to GitHub.\n- Test coverage is currently non-existent - sorry!\n',
    'author': 'Darren Burns',
    'author_email': 'darrenb900@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
