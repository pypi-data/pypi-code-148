# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['otel_cli']

package_data = \
{'': ['*']}

install_requires = \
['Click>=8.1,<9.0',
 'opentelemetry-exporter-otlp>=1.14.0,<1.15.0',
 'opentelemetry-proto>=1.14.0,<1.15.0',
 'opentelemetry-sdk>=1.14.0,<1.15.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.4.0,<4.5.0']}

entry_points = \
{'console_scripts': ['otel = otel_cli.cli:main']}

setup_kwargs = {
    'name': 'otel-cli',
    'version': '0.4.0',
    'description': 'CLI for OpenTelemetry Traces and Metrics in Python',
    'long_description': '# opentelemetry-cli: human-friendly OpenTelemetry CLI\n\n[![License](https://img.shields.io/github/license/dell/opentelemetry-cli?style=flat&color=blue&label=License)](https://github.com/dell/opentelemetry-cli/blob/main/LICENSE)\n[![Pulls](https://img.shields.io/docker/pulls/dell/opentelemetry-cli.svg?logo=docker&style=flat&label=Pulls)](https://hub.docker.com/r/dell/opentelemetry-cli)\n[![PyPI](https://img.shields.io/pypi/v/otel-cli)](https://pypi.org/project/otel-cli/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/dell/opentelemetry-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/dell/opentelemetry-cli)\n[![Docker](https://github.com/dell/opentelemetry-cli/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/dell/opentelemetry-cli/actions/workflows/docker-publish.yml)\n[![Tests](https://github.com/dell/opentelemetry-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/dell/opentelemetry-cli/actions/workflows/tests.yml)\n[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat)](https://gitmoji.dev/)\n\nProvides a CLI for crafting and sending telemetry data over OTLP (OpenTelemetry Line Protocol).\n\n## Requirements\n\n## Installation\n\nThere are several ways of running this CLI.\n\n### Docker\n\n```sh\ndocker pull opentelemetry-cli:<version>\n```\n\nYou can specify a version like `0.2.0` or use `latest` to get the most up-to-date version.\n\nRun latest version of the CLI in a container:\n\n```sh\n# set OTEL_EXPORTER_OTLP_ENDPOINT to your OTel collector instance\nexport OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317\ndocker run --rm -e OTEL_EXPORTER_OTLP_ENDPOINT opentelemetry-cli:latest --help\n```\n\nReplace `--help` with any `otel` command, without `otel` itself.\n\n### PyPI\n\n```sh\npip install otel-cli\n```\n\n## Usage\n\nFirst, define `OTEL_EXPORTER_OTLP_ENDPOINT` in your shell and set it to the OTLP collector instance you want to use.\nFor a local collector, set this to `http://127.0.0.1:4317` like so:\n\n```sh\nexport OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317\n```\n\n### Spans\n\nTo send a span, run:\n\n```sh\notel span "span name"\n```\n\nTo set a different service name, use the `--service` flag:\n\n```sh\notel span --service "My Service" "span name"\n```\n\nYou can also pass custom start and end dates. These should be *nanoseconds* since the epoch:\n\n```sh\nSPAN_START_DATE=$(date --date "2 minutes ago" +%s%N)\nSPAN_END_DATE=$(date +%s%N)\notel span --start "$SPAN_START_DATE" --end "$SPAN_END_DATE" "span name"\n```\n\nBy default, spans are reported with a status of `UNKNOWN`. To pass a different status, use the `--status` option:\n\n```sh\notel span --status OK "successful span"\notel span --status ERROR "failed span"\n```\n\nTo add attributes to spans, use the `--attribute|-a` option. It accepts attributes in a `key=value` format. Use multiple instances of this option to send multiple attributes.\n\n```sh\notel span -a "my.foo=bar" -a "my.bar=baz" "span name"\n```\n\notel will create a random trace ID and span ID. You can override those:\n\n```sh\notel span --trace-id "4d999706756fd1859345f8dc6d0af218" --span-id "ac2a3b2b19ac602d"\n```\n\n#### Sending multiple spans in a trace\n\nTo create a single trace with one root span and multiple child spans, we first need to generate a trace ID for the entire trace and a span ID for the parent span. Use `otel generate` to create those:\n\n```sh\nTRACE_ID=$(otel generate trace_id)\nPARENT_SPAN=$(otel generate span_id)\n```\n\nThen, when creating children span, we pass this information in the format of a `TRACEPARENT`:\n\n```sh\nTRACEPARENT="00-${TRACE_ID}-${PARENT_SPAN}-01"\notel span --traceparent "$TRACEPARENT" "Child A Name"\notel span --traceparent "$TRACEPARENT" "Child B Name"\n```\n\nFinally, send the parent span using the pre-generated IDs:\n\n```sh\notel span --trace-id "$TRACE_ID" --span-id "$PARENT_SPAN" "Parent Span Name"\n```\n\n### Metrics\n\nUse `otel metric` to send metric data. The following metric types are currently supported:\n\n- Counter\n- UpDownCounter\n\n#### Counter\n\nCounters are metrics that can count only up.\nBy specifying just the counter name, it will be incremented by 1:\n\n```sh\notel metric counter my-counter\n```\n\nYou can specify a different value to increase by. For example, this will increase the counter by 1024:\n\n```sh\notel metric counter total-bytes 1024\n```\n\nCounters support attributes just like spans, using the `-a|--attribute` option.\n\n```sh\notel metric counter my-counter -a "host.name=localhost"\n```\n\nBy default, attributes are strings. You can set them to other types by using one of the following prefixes:\n\n- `int:` - value will be converted to an integer.\n- `float:` - value will be converted to a floating point number.\n- `bool:` - value will be converted to a boolean.\n  - Values of `y`, `yes`, `t`, `true`, `on`, and `1` are converted to `True`.\n  - Values of `n`, `no`, `f`, `false`, `off`, and `0` are converted to `False`.\n  - Values are __not__ case-sensitive.\n\nExample:\n\n```sh\notel metric counter my-counter \\\n    -a "key1=just a string" \\\n    -a "int:key2=10" \\\n    -a "float:key3=3.14" \\\n    -a "bool:key4=YES"\n```\n\n#### UpDownCounter\n\nUpDownCounters are metrics that count up or down.\nIf not given a value, the UpDownCounter will increment by one:\n\n```sh\notel metric updown queue-length\n```\n\nYou can specify a different value to increase by. For example, this will increase the counter by 1024:\n\n```sh\notel metric updown my-updowncounter 1024\n```\n\nTo decrease the counter number, pass a negative number like so:\n\n```sh\notel metric updown queue-length -1\n```\n\n## Packaging\nThis project uses [poetry](https://python-poetry.org/) to manage dependencies, build, etc.\n',
    'author': 'Moshi Binyamini',
    'author_email': 'moshi.binyamini@dell.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
