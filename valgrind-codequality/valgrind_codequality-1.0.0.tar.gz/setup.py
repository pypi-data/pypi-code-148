# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valgrind_codequality']

package_data = \
{'': ['*']}

install_requires = \
['xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['valgrind-codequality = '
                     'valgrind_codequality.__main__:main']}

setup_kwargs = {
    'name': 'valgrind-codequality',
    'version': '1.0.0',
    'description': 'Convert Valgrind XML to GitLab Code Quality JSON file.',
    'long_description': '# valgrind-codequality\n\n[![badge-pypi](https://img.shields.io/pypi/v/valgrind-codequality.svg?logo=pypi)](https://pypi.python.org/pypi/valgrind-codequality/)\n&nbsp;\n[![badge-pypi-downloads](https://img.shields.io/pypi/dm/valgrind-codequality)](https://pypi.org/project/valgrind-codequality/)\n\n\n[![badge-pipeline](https://gitlab.com/echopouet/valgrind-codequality/badges/main/pipeline.svg)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)\n&nbsp;\n[![badge-coverage](https://gitlab.com/echopouet/valgrind-codequality/badges/main/coverage.svg)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)\n&nbsp;\n[![badge-pylint](https://gitlab.com/echopouet/valgrind-codequality/-/jobs/artifacts/main/raw/badge.svg?job=pylint)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)\n&nbsp;\n[![badge-formatting](https://gitlab.com/echopouet/valgrind-codequality/-/jobs/artifacts/main/raw/badge.svg?job=format_black)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)\n&nbsp;\n[![badge-issues-cnt](https://img.shields.io/badge/dynamic/json?label=issues&query=statistics.counts.opened&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F19114200%2Fissues_statistics%3Fscope%3Dall)](https://gitlab.com/echopouet/valgrind-codequality/-/issues)\n\n\n## About\n\nI wanted reports from [Valgrind](https://valgrind.org/) to appear in GitLab Merge Requests as [Code Quality reports](https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html#implementing-a-custom-tool), which is a JSON file defined by the Code Quality\'s GitLab.\n\nThat\'s all this does: convert Valgrind XML to Code Quality JSON.\n\nContributions are welcome.\n\n[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/EchoPouet)\n\n### Usage\n\nIt is primarily used as a console script. As such, ensure you have Python 3\'s "scripts" directory in your `PATH` variable.\nFor example, on Linux, that might be `$HOME/.local/bin`.\n\nTo test, try the `--help` or `--version` flags:\n```bash\nvalgrind-codequality --help\n```\n\nThis script follows that example and provides similar command-line options.\nA typical workflow might look like this:\n\n```bash\n# Generate valgrind report as XML\nvalgrind --tool=memcheck --show-leak-kinds=all --track-origins=yes --verbose --xml=yes --xml-file=valgrind_out.xml your_exe\n# Convert to a Code Climate JSON report\nvalgrind-codequality --input-file valgrind_out.xml --output-file valgrind.json\n```\n\nIf you wanted, you could invoke the script directly as a module, like this:\n\n```bash\n# Run as a module instead (note the underscore in the module name here)\npython -m valgrind_codequality --input-file=valgrind_out.xml --output-file=valgrind.json\n```\n\nNow, in your GitLab CI script, [upload this file](https://docs.gitlab.com/ee/ci/pipelines/job_artifacts.html#artifactsreportscodequality)\nas a Code Quality report.\n\n```yaml\nmy-code-quality:\n  script:\n    - [...]\n  artifacts:\n    reports:\n      codequality: valgrind.json\n```\n\n### Contributing\n\n* Sign the contributor agreement (coming soon)\n* Format with [black](https://pypi.org/project/black/)\n* Check with [pylint](https://pypi.org/project/pylint/)\n\n### Credits & Trademarks\n\nvalgrind is an open-source project with a GPL v3.0 license.\n* http://valgrind.sourceforge.net\n* https://github.com/danmar/valgrind\n\n"GitLab" is a trademark of GitLab B.V.\n* https://gitlab.com\n* https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html\n\nAll other trademarks belong to their respective owners.\n',
    'author': 'Arnaud Moura',
    'author_email': 'arnaudmoura@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.8,<=3.12',
}


setup(**setup_kwargs)
