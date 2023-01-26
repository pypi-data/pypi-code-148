# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyro', 'tyro.conf', 'tyro.extras']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'docstring-parser>=0.14.1,<0.15.0',
 'frozendict>=2.3.4,<3.0.0',
 'rich>=11.1.0',
 'shtab>=1.5.6,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['backports.cached-property>=1.0.2,<2.0.0'],
 ':sys_platform == "win32"': ['colorama>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'tyro',
    'version': '0.3.38',
    'description': 'Strongly typed, zero-effort CLI interfaces',
    'long_description': '<br />\n<p align="center">\n    <!--\n    Note that this README will be used for both GitHub and PyPI.\n    We therefore:\n    - Keep all image URLs absolute.\n    - In the GitHub action we use for publishing, strip some HTML tags that aren\'t supported by PyPI.\n    -->\n        <img alt="tyro logo" src="https://brentyi.github.io/tyro/_static/logo-light.svg" width="200px" />\n\n</p>\n\n<p align="center">\n    <em><a href="https://brentyi.github.io/tyro">Documentation</a></em>\n    &nbsp;&nbsp;&bull;&nbsp;&nbsp;\n    <em><code>pip install tyro</code></em>\n</p>\n\n<p align="center">\n    <img alt="build" src="https://github.com/brentyi/tyro/workflows/build/badge.svg" />\n    <img alt="mypy" src="https://github.com/brentyi/tyro/workflows/mypy/badge.svg?branch=main" />\n    <img alt="lint" src="https://github.com/brentyi/tyro/workflows/lint/badge.svg" />\n    <a href="https://codecov.io/gh/brentyi/tyro">\n        <img alt="codecov" src="https://codecov.io/gh/brentyi/tyro/branch/main/graph/badge.svg" />\n    </a>\n    <a href="https://pypi.org/project/tyro/">\n        <img alt="codecov" src="https://img.shields.io/pypi/pyversions/tyro" />\n    </a>\n</p>\n\n<br />\n\n<strong><code>tyro</code></strong> is a tool for building command-line\ninterfaces and configuration objects in Python.\n\nOur core interface, `tyro.cli()`, generates command-line interfaces from\ntype-annotated callables.\n\n---\n\n### Brief walkthrough\n\nTo summarize how `tyro.cli()` can be used, let\'s consider a script based on\n`argparse`. We define two inputs and print the sum:\n\n```python\n"""Sum two numbers from argparse."""\nimport argparse\n\nparser = argparse.ArgumentParser()\nparser.add_argument("--a", type=int, required=True)\nparser.add_argument("--b", type=int, default=3)\nargs = parser.parse_args()\n\ntotal = args.a + args.b\n\nprint(total)\n```\n\nThis pattern is dramatically cleaner than manually parsing `sys.argv`, but has\nseveral issues: it lacks type checking and IDE support (consider: jumping to\ndefinitions, finding references, docstrings, refactoring and renaming tools),\nrequires a significant amount of parsing-specific boilerplate, and becomes\ndifficult to manage for larger projects.\n\nThe basic goal of `tyro.cli()` is to provide a wrapper for `argparse` that\nsolves these issues.\n\n**(1) Command-line interfaces from functions.**\n\nWe can write the same script as above using `tyro.cli()`:\n\n```python\n"""Sum two numbers by calling a function with tyro."""\nimport tyro\n\ndef add(a: int, b: int = 3) -> int:\n    return a + b\n\n# Populate the inputs of add(), call it, then return the output.\ntotal = tyro.cli(add)\n\nprint(total)\n```\n\nOr, more succinctly:\n\n```python\n"""Sum two numbers by calling a function with tyro."""\nimport tyro\n\ndef add(a: int, b: int = 3) -> None:\n    print(a + b)\n\ntyro.cli(add)  # Returns `None`.\n```\n\n**(2) Command-line interfaces from config objects.**\n\nA class in Python can be treated as a function that returns an instance. This\nmakes it easy to populate explicit configuration structures:\n\n```python\n"""Sum two numbers by instantiating a dataclass with tyro."""\nfrom dataclasses import dataclass\n\nimport tyro\n\n@dataclass\nclass Args:\n    a: int\n    b: int = 3\n\nargs = tyro.cli(Args)\nprint(args.a + args.b)\n```\n\nUnlike directly using `argparse`, both the function-based and dataclass-based\napproaches are compatible with static analysis; tab completion and type checking\nwill work out-of-the-box.\n\n**(3) Additional features.**\n\nThese examples only scratch the surface of what\'s possible. `tyro` aims to\nsupport all reasonable type annotations, which can help us define things like\nhierachical structures, enums, unions, variable-length inputs, and subcommands.\nSee [documentation](https://brentyi.github.io/tyro) for examples.\n\n### In the wild\n\n`tyro` is still a new library, but being stress tested in several projects!\n\n- [nerfstudio-project/nerfstudio](https://github.com/nerfstudio-project/nerfstudio/)\n  provides a set of tools for end-to-end training, testing, and rendering of\n  neural radiance fields.\n- [Sea-Snell/JAXSeq](https://github.com/Sea-Snell/JAXSeq/) is a library for\n  distributed training of large language models in JAX.\n- [kevinzakka/obj2mjcf](https://github.com/kevinzakka/obj2mjcf) is an interface\n  for processing composite Wavefront OBJ files for Mujoco.\n- [brentyi/tensorf-jax](https://github.com/brentyi/tensorf-jax/) is an\n  unofficial implementation of\n  [Tensorial Radiance Fields](https://apchenstu.github.io/TensoRF/) in JAX.\n',
    'author': 'brentyi',
    'author_email': 'brentyi@berkeley.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/brentyi/tyro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
