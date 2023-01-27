# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytestarch',
 'pytestarch.diagram_extension',
 'pytestarch.eval_structure',
 'pytestarch.eval_structure_generation',
 'pytestarch.eval_structure_generation.file_import',
 'pytestarch.eval_structure_generation.graph_generation',
 'pytestarch.query_language',
 'pytestarch.rule_assessment',
 'pytestarch.rule_assessment.error_message',
 'pytestarch.rule_assessment.rule_check']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0', 'networkx>=3.0,<4.0']

setup_kwargs = {
    'name': 'pytestarch',
    'version': '1.3.1',
    'description': 'Test framework for software architecture based on imports between modules',
    'long_description': '# Welcome to PyTestArch\n\nPyTestArch is an open source library that allows users to define architectural rules and test their code against them. It is \ngenerally inspired by [ArchUnit](https://www.archunit.org/).\n\n## Installation Guide\nPyTestArch is available via [PyPI](https://pypi.org/project/pytestarch/) and can be installed e.g. via pip: `pip install pytestarch`.\n\n## Usage Guide\nThree steps are required to test an architectural rule:\n\n1) Create an evaluable representation of the source code you want to test\n\n```\nfrom pytestarch.pytestarch import get_evaluable_architecture\n\nevaluable = get_evaluable_architecture("/home/dummy/project", "/home/dummy/project/src")\n```\nThis will scan all python files under /home/dummy/project/src for imports and build an internal representation that can\nlater be queried. The first parameter /home/dummy/project helps PyTestArch to differentiate between internal and external \ndependencies. This evaluable can be used for multiple architectural rule checks; if you are using [pytest](https://docs.pytest.org/en/7.1.x/),\nyou could use a fixture for this evaluable object.\n\n2) Define an architectural rule\n```\nfrom pytestarch.query_language.base_language import Rule\n\nrule = Rule()\n        .modules_that()\n        .are_named("src.moduleB")\n        .should_not()\n        .be_imported_by_modules_that()\n        .are_sub_modules_of("src.moduleA"),\n```\n\nThis rule represents the architectural requirements that a module named "src.moduleB" should not be imported by any module\nthat is a submodule of "src.moduleA", excluding "src.moduleA" itself.\n\n3) Evaluate your code against this rule\n\n```\nrule.assert_applies(evaluable)\n```\nThat\'s it!\n',
    'author': 'zyskarch',
    'author_email': 'zyskarch@gmail.com',
    'maintainer': 'zyskarch',
    'maintainer_email': 'zyskarch@gmail.com',
    'url': 'https://github.com/zyskarch/pytestarch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
