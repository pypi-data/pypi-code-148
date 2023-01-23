# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel',
 'ampel.abstract',
 'ampel.aux',
 'ampel.aux.filter',
 'ampel.cli',
 'ampel.config',
 'ampel.config.builder',
 'ampel.config.collector',
 'ampel.core',
 'ampel.demo',
 'ampel.dev',
 'ampel.ingest',
 'ampel.log',
 'ampel.log.handlers',
 'ampel.metrics',
 'ampel.model',
 'ampel.model.aux',
 'ampel.model.builder',
 'ampel.model.ingest',
 'ampel.model.job',
 'ampel.model.purge',
 'ampel.model.t3',
 'ampel.model.time',
 'ampel.mongo',
 'ampel.mongo.model',
 'ampel.mongo.purge',
 'ampel.mongo.query',
 'ampel.mongo.query.var',
 'ampel.mongo.update',
 'ampel.mongo.update.var',
 'ampel.mongo.view',
 'ampel.ops',
 'ampel.run',
 'ampel.secret',
 'ampel.t1',
 'ampel.t2',
 'ampel.t3',
 'ampel.t3.include.session',
 'ampel.t3.stage',
 'ampel.t3.stage.filter',
 'ampel.t3.stage.project',
 'ampel.t3.supply',
 'ampel.t3.supply.complement',
 'ampel.t3.supply.load',
 'ampel.t3.supply.select',
 'ampel.t3.unit',
 'ampel.template',
 'ampel.test',
 'ampel.util',
 'ampel.vendor.aiopipe']

package_data = \
{'': ['*'], 'ampel.test': ['test-data/*']}

install_requires = \
['ampel-interface>=0.8.3,<0.9.0',
 'appdirs>=1.4.4,<2.0.0',
 'prometheus-client>=0.15,<0.16',
 'psutil>=5.8.0,<6.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pymongo>=4.0,<5.0',
 'schedule>=1.0.0,<2.0.0',
 'sjcl>=0.2.1,<0.3.0',
 'xxhash>=3.0.0,<4.0.0',
 'yq>=3.0.0,<4.0.0']

extras_require = \
{'docs': ['Sphinx>=6.1.2,<6.2.0',
          'sphinx-press-theme>=0.5.1,<0.9.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'tomlkit>=0.11.0,<0.12.0'],
 'server': ['fastapi>=0.89,<0.90', 'uvicorn[standard]>=0.20.0,<0.21.0'],
 'slack': ['slack-sdk>=3.18.1,<4.0.0']}

entry_points = \
{'cli': ['buffer_Match_and_view_or_save_ampel_buffers = '
         'ampel.cli.BufferCommand',
         'config_Build_or_update_config._Fetch_or_append_config_elements = '
         'ampel.cli.ConfigCommand',
         'db_Initialize,_dump,_delete_specific_databases_or_collections = '
         'ampel.cli.DBCommand',
         'event_Show_events_information = ampel.cli.EventCommand',
         'job_Run_schema_file(s) = ampel.cli.JobCommand',
         'log_Select,_format_and_either_view_(tail_mode_available)_or_save_logs '
         '= ampel.cli.LogCommand',
         'process_Run_single_task = ampel.cli.ProcessCommand',
         'run_Run_selected_process(es)_from_config = ampel.cli.RunCommand',
         't2_Match_and_either_reset_or_view_raw_t2_documents = '
         'ampel.cli.T2Command',
         'view_Select,_load_and_save_fresh_"ampel_views" = '
         'ampel.cli.ViewCommand'],
 'console_scripts': ['ampel = ampel.cli.main:main',
                     'ampel-controller = '
                     'ampel.core.AmpelController:AmpelController.main',
                     'ampel-db = ampel.db.AmpelDB:main']}

setup_kwargs = {
    'name': 'ampel-core',
    'version': '0.8.3',
    'description': 'Alice in Modular Provenance-Enabled Land',
    'long_description': '<img align="left" src="https://user-images.githubusercontent.com/17532220/213287939-c3f2db40-9c43-4d4c-8d55-68531cddcad7.png" width="150" height="150"/>\n<br>\n\n# AMPEL-core\n<br><br>\n\n## Information about AMPEL is available [here](https://github.com/AmpelProject)\n',
    'author': 'Valery Brinnel',
    'author_email': 'None',
    'maintainer': 'Jakob van Santen',
    'maintainer_email': 'jakob.van.santen@desy.de',
    'url': 'https://ampelproject.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
