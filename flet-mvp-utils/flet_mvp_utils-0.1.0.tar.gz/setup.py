# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flet_mvp_utils']

package_data = \
{'': ['*']}

install_requires = \
['flet>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'flet-mvp-utils',
    'version': '0.1.0',
    'description': 'Tools to build flet apps with the MVP architecture pattern',
    'long_description': "# flet-mvp-utils\n\nThis library provides tools that make it a bit easier\nto follow architecture patterns in your flet app\nthat leverage on immutable models and unidirectional control flow.\nThose are mostly based on the Model-View-Presenter/MVP pattern,\nhence the name of the library.\nAt this stage,\nit can be used to ease working with any model-based architecture pattern though.\n\n## Assumptions/usage\n\nYour model is a dataclass (ideally an immutable/frozen one).\nSome kind of broker is subscribed to be notified of\nany change of the current model of e.g. the data source that holds\nand modifies it/creates updated models.\nThis is done with the help of the `Observable` class.\nThe data source inherits from it,\nthe broker (or presenter in MVP terms) registers a callback with it\nand when the data source updates/replaces its model,\nit notifies the presenter (and other subscribed observers).\n\nYour view uses [refs](https://flet.dev/docs/guides/python/control-refs/).\nThe actual UI code may be located somewhere else\nand simply receive the refs and return a component that is connected to the ref.\nWhen creating the view class, you inherit from `MvpView`\nand in your `__init__.py`, you create a dictionary that maps the attribute names\nof your model dataclass to the respective ref\nof the control that should be tied to it.\nYou then pass this dictionary to `super().__init__()`,\nalong with any variable intended for the `flet.View` constructor.\n`MvpView` has a `render(model)` method that takes a model\nand updates any refs current value to the model value if they aren't the same.\nThis method is supposed to be called in the callback\nyou register with the data source,\nso that a changed model is immediately reflected in the view.\n",
    'author': 'iron3oxide',
    'author_email': 'jason.hottelet@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
