# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['promql_http_api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22,<0.24']

setup_kwargs = {
    'name': 'promql-http-api',
    'version': '0.1.1',
    'description': 'Query a Prometheus server and get a Pandas DataFrame',
    'long_description': "# PromQL HTTP API\n\nThis python package provides a [Prometheus](https://prometheus.io/) HTTP API client library.\nIt encapsulates and simplifies the collection of data from a Prometheus server.\nOne major feature of this library is that responses to queries are returned as [Pandas](https://pandas.pydata.org/) DataFrames.\n\nPrometheus \n\n## Installation\n\nTo install as a root user:\n\n```commandline\npython3 -m pip install promql-http-api\n```\n\nTo install as a non-root user:\n\n```commandline\npython3 -m pip install --user promql-http-api\n```\n\nTo uninstall:\n```commandline\npython3 -m pip uninstall promql-http-api\n```\n\n## Usage Examples\n\nHere is a basic usage example:\n\n```python\nfrom promql_http_api import PromqlHttpApi\n\napi = PromqlHttpApi('http://localhost:9090')\nq = api.query('up', '2020-01-01T12:00:00Z')\ndf = q.to_dataframe()\nprint(df)\n```\n\nOn the first line we create a PromqlHttpApi object named `api`. This example assumes that a Prometheus server is running on the local host, and it is listening to port 9090.\nReplace this URL as needed with the appropriate URL for your server.\n\nNext, we use the `api` object to create a Query object named `q`. The `query()` function takes two parameters: a query string and a date-time string.\n\nTo execute the query explicitly, without converting the result to a DataFrame, you can use:\n```python\n# Execute the query explicitly\npromql_response_data = q()\n\n# Convert the cached result to a DataFrame\ndf = q.to_dataframe()\n```\n\nAlternately, by calling the to_dataframe() method alone, we will implicitly execute the query.\n\n```python\n# Execute the query implicitly\ndf = q.to_dataframe()\n```\n\n## Debugging\n\nIf something goes wrong, you can look at the HTTP response and the PromQL response information. Here are some examples:\n```python\nfrom promql_http_api import PromqlHttpApi\napi = PromqlHttpApi('http://localhost:9090')\nq = api.query('up', '2020-01-01T12:00:00Z')\nq()\npromql_response = q.response\nhttp_response = promql_response.response\nprint(f'HTTP response status code  = {http_response.status_code}')\nprint(f'HTTP response encoding     = {http_response.encoding}')\nprint(f'PromQL response status     = {promql_response.status()}')\nprint(f'PromQL response data       = {promql_response.data()}')\nprint(f'PromQL response error type = {promql_response.error_type()}')\nprint(f'PromQL response error      = {promql_response.error()}')\n```\n\n---\n# List of Supported APIs\n\n| API                               | Method           | Arguments |\n|---------------------              |------------------|---\n| /api/v1/query                     | query()          | query, time\n| /api/v1/query_range               | query_range()    | query, start, end, step\n| /api/v1/format_query              | format_query()   | query\n| /api/v1/series                    | series()         | match\n| /api/v1/labels                    | labels()         |\n| /api/v1/label/<label_name>/values | label_values()   | label\n| /api/v1/targets                   | targets()        | state\n| /api/v1/rules                     | rules()          | type\n| /api/v1/alerts                    | alerts()         |\n| /api/v1/alertmanagers             | alertmanagers()  |\n| /api/v1/status/config             | config()         |\n| /api/v1/status/flags              | flags()          |\n| /api/v1/status/runtimeinfo        | runtimeinfo()    |\n| /api/v1/status/buildinfo          | buildinfo()      |\n\n\n---\n# Testing\n\nThe package contains limited unit testing.\nRun the tests from the package top folder using:\n\n```commandline\npytest\n```\n\n---\n# Future work\n\nImplement a CI/CD pipeline with a Prometheus instance in a Docker container to test API accesses.\n\nIf you use this library and would like to help - please contact the author.\n\n---\n# References\n\n[Prometheus / HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/)\n",
    'author': 'Nir Arad',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nir-arad/promql-http-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
