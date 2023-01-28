# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_fluentui_components']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.7.0']}

setup_kwargs = {
    'name': 'dash-fluentui-components',
    'version': '0.0.3',
    'description': 'FluentUI components for Plotly Dash.',
    'long_description': '# dash-fluentui-components\n\nA component library for Plotly\'s Dash based on the fluentui react components.\n\n## Installation\n\n```sh\npoetry add dash-fluentui-components\n```\n\nor via pip\n\n```sh\npip install dash-fluentui-components\n```\n\n## Usage\n\n```py\nfrom dash import Dash, Input, Output, callback, callback_context\nfrom dash.exceptions import PreventUpdate\n\nimport dash_fluentui_components as dfc\n\napp = Dash(__name__)\n\nopen_dialog = dfc.Button("OpenDialog", id="open-id")\nclose_dialog = dfc.Button("CloseDialog", id="close-id")\ndialog = dfc.Dialog(\n    "Content",\n    title="A dialog component",\n    trigger=open_dialog,\n    trigger_action=close_dialog,\n)\n\npage1 = dfc.Page(dfc.Button("Button 1"), page_key="page-1", controls=dialog)\npage2 = dfc.Page(dfc.Button("Button 2"), page_key="page-2", controls=dfc.Button("Control 2"))\n\napp.layout = dfc.FluentProvider(theme="dark", children=dfc.PagesWithSidebar([page1, page2], selected_key="page-1"))\n\nif __name__ == "__main__":\n    app.run_server(debug=True)\n\n```\n\n## TODO\n\n- [smooth sidebar transitions][smmoth]\n\n[smmoth]: http://reactcommunity.org/react-transition-group/\n',
    'author': 'Robert Pack',
    'author_email': 'robstar.pack@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
