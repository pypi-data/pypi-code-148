# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybond']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybond',
    'version': '0.1.3',
    'description': 'pybond is a spying and stubbing library inspired by the clojure bond library.',
    'long_description': '# pybond\n\n[![Build](https://github.com/epgui/pybond/actions/workflows/build.yml/badge.svg)](https://github.com/epgui/pybond/actions/workflows/build.yml)\n[![codecov](https://codecov.io/github/epgui/pybond/branch/main/graph/badge.svg?token=tkq655ROg3)](https://app.codecov.io/github/epgui/pybond)\n\n`pybond` is a spying and stubbing library inspired heavily by the\n[clojure `bond` library](https://github.com/circleci/bond/).\n\n## Installation\n\npip\n\n```bash\npip install pybond==0.1.3\n```\n\nrequirements.txt\n\n```python\npybond==0.1.3\n```\n\npyproject.toml\n\n```toml\npybond = "0.1.3"\n```\n\n## Example usage\n\nLet\'s say you wanted to test the functions in this module:\n\n```python\n# /tests/sample_code/my_module.py\nfrom typing import Any\nimport tests.sample_code.other_package as other_package\n\n\ndef foo(x: Any) -> None:\n    response = other_package.make_a_network_request(x)\n    other_package.write_to_disk(response)\n    return response\n\n\ndef bar(x: Any) -> None:\n    return foo(x)\n```\n\nWith `pybond` you can easily spy on any given function or stub out functions\nthat perform IO:\n\n```python\n# /tests/test_my_module.py\nfrom pybond import calls, called_with_args, spy, stub, times_called\n\nimport tests.sample_code.other_package as other_package\nimport tests.sample_code.my_module as my_module\nfrom tests.sample_code.my_module import bar\n\n\ndef test_foo_is_called():\n    with spy([my_module, "foo"]):\n        assert times_called(my_module.foo, 0)\n        bar(42)\n        assert times_called(my_module.foo, 1)\n        bar(42)\n        bar(42)\n        assert times_called(my_module.foo, 3)\n\n\ndef test_bar_handles_response():\n    with stub(\n        [other_package, "make_a_network_request", lambda x: {"result": x * 2}],\n        [other_package, "write_to_disk", lambda _: None],\n    ), spy(\n        [my_module, "foo"],\n    ):\n        assert times_called(my_module.foo, 0)\n        assert times_called(other_package.make_a_network_request, 0)\n        assert bar(21) == {"result": 42}\n        assert times_called(my_module.foo, 1)\n        assert times_called(other_package.make_a_network_request, 1)\n        assert called_with_args(my_module.foo, args=[21])\n        assert bar(20) == {"result": 40}\n        assert calls(my_module.foo) == [\n            {\n                "args": [21],\n                "kwargs": None,\n                "return": {"result": 42},\n                "error": None,\n            },\n            {\n                "args": [20],\n                "kwargs": None,\n                "return": {"result": 40},\n                "error": None,\n            },\n        ]\n        assert calls(other_package.write_to_disk) == [\n            {\n                "args": [{"result": 42}],\n                "kwargs": None,\n                "return": None,\n                "error": None,\n            },\n            {\n                "args": [{"result": 40}],\n                "kwargs": None,\n                "return": None,\n                "error": None,\n            },\n        ]\n```\n\n## License\n\nDistributed under the\n[Eclipse Public License](http://www.eclipse.org/legal/epl-v10.html).\n',
    'author': 'Guillaume Pelletier',
    'author_email': 'guigui.p@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/epgui/pybond',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
