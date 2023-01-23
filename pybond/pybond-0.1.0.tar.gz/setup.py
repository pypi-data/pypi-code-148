# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybond']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybond',
    'version': '0.1.0',
    'description': 'pybond is a spying and stubbing library inspired by the clojure bond library.',
    'long_description': '# pybond\n\n`pybond` is a spying and stubbing library inspired heavily by the\n[clojure `bond` library](https://github.com/circleci/bond/).\n\n```python\n# src/my_module.py\nfrom typing import Any\nfrom other_package import make_a_network_request, write_to_disk\n\n\ndef foo(x: Any) -> None:\n    response = make_a_network_request(x)\n    write_to_disk(response)\n    return response\n\n\ndef bar(x: Any) -> None:\n    return foo(x)\n```\n\n```python\n# tests/test_my_module.py\nfrom bond import calls, called_with_args, spy, stub, times_called\n\nimport other_package\nimport src.my_module\nfrom src.my_module import bar\n\n\ndef test_foo_is_called():\n    with spy([src.my_module, "foo"]):\n        assert times_called(src.my_module.foo, 0)\n        bar(42)\n        assert times_called(src.my_module.foo, 1)\n        bar(42)\n        bar(42)\n        assert times_called(src.my_module.foo, 3)\n\n\ndef test_bar_handles_response():\n    with stub(\n        [other_package, "make_a_network_request", lambda x: {"result": x * 2}],\n        [other_package, "write_to_disk", lambda _: None],\n    ), spy(\n        [src.my_module, "foo"],\n    ):\n        assert times_called(src.my_module.foo, 0)\n        assert times_called(other_package.make_a_network_request, 0)\n        assert bar(21) == 42\n        assert times_called(src.my_module.foo, 1)\n        assert times_called(other_package.make_a_network_request, 1)\n        assert called_with_args(src.my_module.foo, args=[21])\n        assert bar(20) == 40\n        assert calls(src.my_module.foo) == [\n            {"args": [21] "kwargs": None "return": 42 "error": None},\n            {"args": [20] "kwargs": None "return": 40 "error": None},\n        ]\n```\n\n## License\n\nDistributed under the\n[Eclipse Public License](http://www.eclipse.org/legal/epl-v10.html).\n',
    'author': 'Guillaume Pelletier',
    'author_email': 'guigui.p@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/epgui/pybond',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
