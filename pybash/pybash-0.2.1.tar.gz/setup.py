# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pybash']
install_requires = \
['ideas>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'pybash',
    'version': '0.2.1',
    'description': '>execute bash commands from python easily',
    'long_description': '# PyBash\n\nStreamline bash-command execution from python with an easy-to-use syntax. It combines the simplicity of writing bash scripts with the flexibility of python. Under the hood, any line or variable assignment starting with `>` or surrounded by parentheses is transformed to python `subprocess` calls and then injected into `sys.meta_path` as an import hook. All possible thanks to the wonderful [ideas](https://github.com/aroberge/ideas) project!\n\nFor security and performance reasons, PyBash will NOT execute as shell, unless explicitly specified with a `$` instead of a single `>` before the command. While running commands as shell can be convenient, it can also spawn security risks and  if you\'re not too careful. If you\'re curious about the transformations, look at the [unit tests](test_pybash.py) for some quick examples.\n\nNote: this is a mainly experimental library. Consider the risks and test before using in prod.\n\n# Installation\n`pip install pybash`\n\n# Setup hook\n```python\nimport pybash\npybash.add_hook()\n```\n\n# Usage\n\n### 1. Simple execution with output\n```python\n>python --version\n>echo \\\\nthis is an echo\n```\noutputs:\n```\nPython 3.9.15\n\nthis is an echo\n```\n\n### 2. Set output to variable and parse\n```python\nout = >cat test.txt\ntest_data = out.decode(\'utf-8\').strip()\nprint(test_data.replace("HELLO", "HOWDY"))\n```\noutputs:\n```\nHOWDY WORLD\n```\n\n### 3. Wrapped, in-line execution and parsing\n```python\nprint((>cat test.txt).decode(\'utf-8\').strip())\n```\noutputs:\n```\nHELLO WORLD\n```\n\n### 4. Redirection\n```python\n>echo "hello" >> test4.txt\n```\n\n### 5. Pipe chaining\n```python\n>cat test.txt | sed \'s/HELLO/HOWDY/g\' | sed \'s/HOW/WHY/g\' | sed \'s/WHY/WHEN/g\'\n```\noutputs:\n```\nWHENDY WORLD\n```\n\n### 6. Redirection chaining\n```python\n>cat test.txt | sed \'s/HELLO/HOWDY\\\\n/g\' > test1.txt >> test2.txt > test3.txt\n```\n\n### 7. Chaining pipes and redirection- works in tandem!\n```python\n>cat test.txt | sed \'s/HELLO/HOWDY\\\\n/g\' > test5.txt\n```\n\n### 8. Input redirection\n```python\n>sort < test.txt >> sorted_test.txt\n```\n\n```python\n>sort < test.txt | sed \'s/SORT/TEST\\\\n/g\'\n```\n### 9. Glob patterns with shell\n```python\n$ls .github/*\n```\n\n#### Also works inside methods!\n```python\n# PYBASH DEMO #\ndef cp_test():\n    >cp test.txt test_copy.txt\n\ncp_test()\n```\n\n# Dev\n\n#### Demo\n`python run.py`\n\n#### Debugging\n`python -m ideas demo -a pybash -s` to view the transformed source code\n',
    'author': 'Jay',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
