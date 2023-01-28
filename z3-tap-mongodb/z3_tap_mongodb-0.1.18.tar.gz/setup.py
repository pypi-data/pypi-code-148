# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_mongodb', 'tap_mongodb.tests']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['orjson>=3.8.2',
 'pymongo[srv]>=4.3.3',
 'requests>=2.25.1',
 'singer-sdk>=0.17.0']

entry_points = \
{'console_scripts': ['tap-mongodb = tap_mongodb_z.tap:TapMongoDB.cli']}

setup_kwargs = {
    'name': 'z3-tap-mongodb',
    'version': '0.1.18',
    'description': 'z3-tap-mongodb is a Singer tap for MongoDB, built with the Meltano SDK for Singer Taps.',
    'long_description': '# tap-mongodb\n\n`tap-mongodb` is a Singer tap for MongoDB.\n\nBuilt with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.\n\n## Installation\n\n```bash\npipx install git+https://github.com/z3z1ma/tap-mongodb.git\n```\n\n## Configuration\n\n### Accepted Config Options\n\n| Setting             | Required | Default | Description |\n|:--------------------|:--------:|:-------:|:------------|\n| prefix              | False    |    ""   | Optionally add a prefix for all streams, useful if ingesting from multiple shards/clusters via independent tap-mongodb configs. |\n| ts_based_replication| False    |    []   | A list of stream names. A stream mentioned here indicates it uses timestamp-based replication. The default for a stream is ❗️ non-timestamp based since Mongo most often uses epochs. This overriding approach is required since the determination of timestamp based replication requires the key exist in the jsonschema with a date-like type which is impossible when there is no explicit schema prior to runtime. NOTE: Streams still require `metadata` mapping with an explicit callout of `replication-key` and `replication-method`. |\n| mongo               | True     | None    | User-defined props. These props are passed directly to pymongo MongoClient allowing the tap user full flexibility not provided in any other Mongo tap. |\n| resilient_replication_key | False    | False    | This setting allows the tap to continue processing if a document is missing the replication key. Useful if a very small percentage of documents are missing the prop. Subsequent executions with a bookmark will ensure they only ingested once. |\n| stream_maps         | False    | None    |             |\n| stream_map_settings | False    | None    |             |\n| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |\n| flattening_enabled  | False    | None    | \'True\' to enable schema flattening and automatically expand nested properties. |\n| flattening_max_depth| False    | None    | The max depth to flatten schemas. |\n\nA full list of supported settings and capabilities for this\ntap is available by running:\n\n```bash\ntap-mongodb --about\n```\n\n### Configure using environment variables\n\nThis Singer tap will automatically import any environment variables within the working directory\'s\n`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching\nenvironment variable is set either in the terminal context or in the `.env` file.\n\n### Capabilities\n\n* `catalog`\n* `state`\n* `discover`\n* `about`\n* `stream-maps`\n* `schema-flattening`\n\n## Usage\n\nYou can easily run `tap-mongodb` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-mongodb --version\ntap-mongodb --help\ntap-mongodb --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tap_mongodb/tests` subfolder and\n  then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-mongodb` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-mongodb --help\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\nYour project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in\nthe file.\n\nNext, install Meltano (if you haven\'t already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-mongodb\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-mongodb --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-mongodb target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to\ndevelop your own taps and targets.\n',
    'author': 'Alex Butler',
    'author_email': 'butler.alex2010@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/z3z1ma/tap-bigquery',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
