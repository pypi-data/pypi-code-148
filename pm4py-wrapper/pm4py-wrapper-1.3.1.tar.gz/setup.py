# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pm4py_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'cvxopt>=1.3.0,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pm4py>=2.3,<2.4',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.0.1,<8.0.0',
 'scipy>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['pm4py_wrapper = pm4py_wrapper.cli:main']}

setup_kwargs = {
    'name': 'pm4py-wrapper',
    'version': '1.3.1',
    'description': 'pm4py wrapper to call the original package from CLI',
    'long_description': '# pm4py-wrapper\n\n![Build & Test](https://github.com/AutomatedProcessImprovement/pm4py-wrapper/actions/workflows/build_test.yml/badge.svg)\n\nCLI wrapper for pm4py.\n\n## Installation\n\nInstall using [pip](https://pip.pypa.io/en/stable/installation/):\n\n```shell\npip install pm4py-wrapper\n```\n\n### Known Issues for macOS with M1\n\n#### cvxopt@1.3.0: umfpack.h is missing\n\n- Discussion is at https://github.com/cvxopt/cvxopt/issues/78.\n- Solution:\n  - Install `suite-sparse`\n  - Specify `CPPFLAGS` and `LDFLAGS`\n  - Run `pip install cvxopt`\n- More details at http://cvxopt.org/install/index.html\n\n```shell\n$ brew info suite-sparse\n$ export CPPFLAGS="-I/opt/homebrew/include/"\n$ export LDFLAGS="-L/opt/homebrew/lib"\n$ pip install cvxopt\n```\n\n#### scipy@1.6.1\n\n- Discussion is at https://github.com/scipy/scipy/issues/13409\n- Solution: use a newer version starting from 1.7.0\n\n## Usage\n\n```\nUsage: pm4py_wrapper [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -i, --input_log PATH   Path to the input event log.  [required]\n  -o, --output_dir PATH  Path to the output directory.\n  --help                 Show this message and exit.\n\nCommands:\n  csv-to-xes\n  xes-to-csv\n\n```\n\nExamples:\n\n```shell\n$ pm4py_wrapper -i tests/assets/input/Production.xes -o tests/assets/output xes-to-csv\n$ pm4py_wrapper -i tests/assets/input/Production.csv -o tests/assets/output csv-to-xes\n```\n\n## Links\n\n- A helpful [answer](https://stackoverflow.com/questions/57628064/automating-python-package-release-process#answer-57676367) on StackOverflow on how to do CI/CD with Poetry.\n',
    'author': 'Ihar Suvorau',
    'author_email': 'ihar.suvorau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
