# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_rst']
entry_points = \
{'pytest11': ['pytest-rst = pytest_rst']}

setup_kwargs = {
    'name': 'pytest-rst',
    'version': '0.1.5',
    'description': 'Test code from RST documents with pytest',
    'long_description': '.. image:: https://github.com/mosquito/pytest-rst/workflows/tests/badge.svg\n   :target: https://github.com/mosquito/pytest-rst/actions?query=workflow%3Atests\n   :alt: Actions\n\n.. image:: https://img.shields.io/pypi/v/pytest-rst.svg\n   :target: https://pypi.python.org/pypi/pytest-rst/\n   :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/wheel/pytest-rst.svg\n   :target: https://pypi.python.org/pypi/pytest-rst/\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest-rst.svg\n   :target: https://pypi.python.org/pypi/pytest-rst/\n\n.. image:: https://img.shields.io/pypi/l/pytest-rst.svg\n   :target: https://pypi.python.org/pypi/pytest-rst/\n\n\npytest-rst run python tests in ReStructuredText\n===============================================\n\nCode block must have ``:name:`` attribute starts with ``test_``.\n\nExample\n-------\n\nThis block will running as a pytest test-case:\n\n.. code-block:: rst\n\n    .. code-block:: python\n        :name: test_first\n\n        assert True\n\n\n.. code-block:: python\n    :name: test_first\n\n    assert True\n\n\nThis block just not running:\n\n.. code-block:: rst\n\n    .. code-block:: python\n\n        # not a test\n        assert False\n\n.. code-block:: python\n\n    # not a test\n    assert False\n\n\nVersioning\n----------\n\nThis software follows `Semantic Versioning`_\n\n\n.. _Semantic Versioning: http://semver.org/\n',
    'author': 'Dmitry Orlov',
    'author_email': 'me@mosquito.su',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mosquito/pytest-rst',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
