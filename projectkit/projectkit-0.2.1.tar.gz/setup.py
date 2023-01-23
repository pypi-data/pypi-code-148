# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['projectkit', 'projectkit.model', 'projectkit.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'tomlkit>=0.11.6,<0.12.0']

setup_kwargs = {
    'name': 'projectkit',
    'version': '0.2.1',
    'description': '',
    'long_description': '# ProjectKit: File-based settings utility\n\nSupporting both YAML and TOML, your projects will have a user-friendly settings file. Native support for `Pydantic.model` in addition to Python `class`.\n\n## Usage\nThe following generates two new files; `project_kit_demo.toml` and `project_kit_demo.lock.toml`\n```python\nfrom projectkit.model.settings import ProjectKitSettings\n\nmy_settings = ProjectKitSettings(project_name="showing_off", manual_setting_to_default={"leader_age": 96})\n\nwild_user_input = int(input("How many participants? "))\nnumber_of_participants = {\n    "participants": [{"name": "", "age": 0} for _ in range(wild_user_input)]\n}\nmy_settings.dump_new(project_directory=".", additional_settings=number_of_participants)\n```\n\n### Output\n1. The settings file, `project_kit_demo.toml`:\n```toml\nleader_age = 96\n\n[participants]\nname = "age"\n```\n2. The settings lock file, `project_kit_demo.lock.toml`:\n```toml\nPython_version = "3.10.9"\n\n[ProjectKit]\nformat = "toml"\nversion = "0.1.0"\n\n[Locked]\nleader_age = 96\n\n[Locked.participants]\nname = "age" \n```\n\n## Installation\n```shell\npip install projectkit\n```\nFor those that prefer poetry:\n```shell\npoetry add projectkit\n```\n',
    'author': 'caniko',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
