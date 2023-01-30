# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dabapush',
 'dabapush.Configuration',
 'dabapush.Reader',
 'dabapush.Writer',
 'smo-database',
 'smo-database.db_configuration',
 'smo-database.dboes',
 'smo-database.facebook',
 'smo-database.instagram',
 'smo-database.telegram',
 'smo-database.twitter']

package_data = \
{'': ['*'],
 'smo-database': ['data/facebook/*',
                  'data/instagram/1617823/*',
                  'data/instagram/1617823/111322/*',
                  'data/instagram/1617823/177607/*',
                  'data/instagram/1617823/264177/*',
                  'data/instagram/1617823/264202/*',
                  'data/instagram/1617823/264207/*',
                  'data/instagram/1617823/292905/*',
                  'data/instagram/1617823/70200/*',
                  'data/instagram/1617823/70202/*',
                  'data/twitter/parliamentarians/175306005/*',
                  'data/twitter/parliamentarians/770959228450340865/*',
                  'data/twitter/parliamentarians/988692552927928320/*']}

install_requires = \
['PyYAML',
 'SQLAlchemy',
 'click',
 'importlib-metadata',
 'loguru',
 'pandas',
 'psycopg2-binary',
 'ujson']

entry_points = \
{'console_scripts': ['dabapush = dabapush.main:cli'],
 'dabapush077': ['CSV = dabapush.Writer.CSVWriter:CSVWriter',
                 'Twacapic = dabapush.Reader.TwacapicReader:TwacapicReader']}

setup_kwargs = {
    'name': 'dabapush',
    'version': '0.3.1',
    'description': '',
    'long_description': "# dabapush\n\nDatabase pusher for social media data (Twitter for the beginning) – pre-alpha version\n\n## Using dabapush\n\n`dabapush` is a tool to read longer running data collections and write them to another file format or persist them into a database. It is designed to run periodically, e.g. controlled by chron, thus, for convenience ot use project-based configurations which contain all required information on what to read where and what to do with it.\nA **project** may have one or more **jobs**, each job consists of a reader and a writer configuration, e.g. read JSON-files from the Twitter API that we stored in folder `/home/user/fancy-project/twitter/` and write the flattened and compiled data set in to `/some/where/else` as CSV files.\n\n### First steps\n\nIn order to run a first `dabapush`-job we'll need to create a project configuration. This is done by calling:\n\n```bash\ndabapush create\n```\n\nBy default this walks you through the configuration process in a step-by-step manner. Alternatively, you could call:\n\n```bash\ndabapush create --non-interactive\n```\n\nThis will create an empty configuration, you'll have to fill out the required information by e.g. calling:\n\n```bash\ndabapush reader add NDJSON default\ndabapush writer add CSV default\n```\n\nWhereas `reader add`/`writer add` is the verb, `NDJSON` or `CSV` is the plugin to add and `default` is the pipeline name.\n\nOf course you can edit the configration after creation in your favorite editor, but **BEWARE NOT TO TEMPER WITH THE YAMl-TAGS!!!**.\n\nTo run the newly configured job, please call:\n\n```bash\ndabapush run default\n```\n\n## Command Reference\n\n### Invocation Pattern\n\n```bash\ndabapush <command> <subcommand?> <options>\n```\n\n### Commands\n\n`create` -- creates a dabapush project (invokes interactive prompt)\n\nOptions:\n\n`--non-interactive`, create an empty configuration and exit\n\n`--interactive`, *this is the default behavior*: prompts for user input on\n\n- project name,\n- project authors name,\n- project author email address(es) for notifications\n- manually configure targets or run discover?\n\n----\n\n`run all` -- collect all known items and execute targets/destinations\n\n`run <target>` -- run a single writer and/or named target\n\nOptions:\n\n`--force-rerun, -r`: forces all data  to be read, ignores already logged data\n\n----\n\n`update` -- update items for target(s)\n\n`update <target>` or `update all` -- update the target's files-to-be-read list\n\n----\n\n`reader` -- interact with readers\n\n`reader configure <name>` -- configure the reader for one or more subproject(s); Reader configuration is inherited from global to local level; throws if configuration is incomplete and defaults are missing\n\n`reader list`: returns a table of all configured readers, with `<path> <target> <class> <id>`\n\n`reader list_all`: returns a table of all registered reader plugins\n\n`reader add <type> <name>`: add a reader to the project configuration\n\nOptions:\n\n`--input-directory <path>`: directory to be read\n\n`--pattern <pattern>`: pattern for matching file names against.\n\n`remove <name>`: remove a reader from the project configuration.\n\n`register <path>`: not there yet\n\n----\n\n`discover` -- discover (possible) targets in project directory and configure them automagically -- yeah, you dream of that, don't you?\n\n----\n\n`writer` -- interact with writers\n\n`writer add <type> <name>`:\n\n`writer remove <name>`: removes the writer for the given name\n\n`writer list` -- returns table of all writers, with `<path> <subproject-name> <class> <id>`\n\n`writer list_all`: returns a table of all registered writer plugins\n\n`writer configure <name>` or `writer configure all`\n\nOptions:\n\n`--output-dir, -o <path>`: default for all targets: `<project-dir>/output/<target-name>`\n\n`--output-pattern, -p <pattern>`: pattern used for file name creation e.g. 'YYYY-MM-dd', file extension is added by the writer and cannot be overwritten\n\n`--roll-over, -r ``<file-size>`:\n\n`--roll-over, -r` `<lines>`:\n\n`--roll-over -r <None>`: should be the output chunked? Give either a file-size or a number of lines for roll-over or None to disable chunking\n\n`writer register <path> <class-name>`: something for the roadmap.\n\n`deregister <name> <registry-name>`: something for the roadmap.\n\n## Programmatic documention\n\n## Extending dabapush and developers guide\n\n### dabapush's Approach to Projects and Configuration\n\n### Class References\n\n| **Dabapush** |     |\n| ------------ | --- |\n|              |     |\n|              |     |\n|              |     |\n|              |     |\n\n| **Reader** |     |\n| ---------- | --- |\n|            |     |\n|            |     |\n|            |     |\n|            |     |\n\n| **Writer** |     |\n| ---------- | --- |\n|            |     |\n|            |     |\n|            |     |\n|            |     |\n\n| **Configuration** |     |\n|                   |     |\n| ----------------- | --- |\n|                   |     |\n|                   |     |\n|                   |     |\n|                   |     |\n\n### Developer Installation\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the cloned repository's root directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n5. Run `dabapush create` to create your first project.\n6. Run `pytest` to run all tests\n",
    'author': 'Philipp Kessling',
    'author_email': 'p.kessling@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/dabapush',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
