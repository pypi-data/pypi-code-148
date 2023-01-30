# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_great_expectations', 'odd_great_expectations.dataset']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.17,<2.0',
 'great-expectations>=0.15.44,<0.16.0',
 'odd-models>=2.0.10,<3.0.0',
 'oddrn-generator==0.1.62',
 'psycopg2>=2.9.5,<3.0.0',
 'sqlalchemy>=1.4.46,<2.0.0']

setup_kwargs = {
    'name': 'odd-great-expectations',
    'version': '0.1.1',
    'description': 'OpenDataDiscovery Action for Great Expectations',
    'long_description': "## OpenDataDiscovery Great Expectations metadata collecting.\n\n\n## Supporting\n| Feature                     | Supporting |\n| --------------------------- | ---------- |\n| V3 API +                    | +          |\n| SqlAlchemyEngine            | +          |\n| PandasEngine                | +          |\n| Great Expectations V2 API - | -          |\n| Cloud Solution              | -          |\n\n\n`odd_great_expectation.action.ODDAction`\nIs a class derived from `ValidationAction` and can be used in checkpoint actions lists.\n\n## How to:\n\n### Install odd-great-expectations package\n```bash\npip install odd-great-expectations\n```\n\n### Add action to checkpoint:\n```yaml\nname: <CHECKPOINT_NAME>\nconfig_version: 1.0\ntemplate_name:\nmodule_name: great_expectations.checkpoint\nclass_name: Checkpoint\nrun_name_template: '%Y%m%d-%H%M%S-my-run-name-template'\nexpectation_suite_name:\nbatch_request: {}\naction_list:\n  # other actions\n  - name: store_metadata_to_odd \n    action:\n      module_name: odd_great_expectations.action\n      class_name: ODDAction\n      platform_host: <PLATFORM_HOST> # OpenDataDiscovery platform, i.e. http://localhost:8080\n      platform_token: <PLATFORM_TOKEN> # OpenDataDiscovery token\n      data_source_name: <DATA_SOURCE_NAME> # Unique name for data source, i.e. local_qa_test\nevaluation_parameters: {}\n```\n\n### Run checkpoint\n```bash\ngreat_expectations checkpoint run <CHECKPOINT_NAME> \n```\n### Check result\nCheck results on <PLATFORM_HOST> UI.\n\n\n",
    'author': 'Pavel Mackarichev',
    'author_email': 'vixtir90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
