# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcr_langchain']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.66,<0.0.67', 'vcrpy>=4.2.1,<5.0.0']

setup_kwargs = {
    'name': 'vcr-langchain',
    'version': '0.0.3',
    'description': 'Record and replay LLM interactions for langchain',
    'long_description': '# VCR langchain\n\nAdapts [VCR.py](https://github.com/kevin1024/vcrpy) for use with [langchain](https://github.com/hwchase17/langchain) so that you can record and replay all your expensive LLM interactions for tests.\n\n## Quickstart\n\n```bash\npip install vcr-langchain\n```\n\nUse it with pytest:\n\n```python\nimport vcr_langchain as vcr\nfrom langchain.llms import OpenAI\n\n@vcr.use_cassette()\ndef test_use_as_test_decorator():\n    llm = OpenAI(model_name="text-ada-001")\n    assert llm("Tell me a surreal joke") == "<put the output here>"\n```\n\nThe next time you run it:\n\n- the output is now deterministic\n- it executes a lot faster by replaying from cache\n- you no longer need to have the real OpenAI API key defined\n\nFor more examples, see [the usages test file](tests/test_usage.py).\n\n### Why not just use VCR.py directly?\n\nThis offers higher-level, more human-readable recordings for inspection. Additionally, I plan to support recording of utilities as well, which includes non-network requests such as command executions inside Bash or the Python REPL.\n\n## Documentation\n\nFor more information on how VCR works and what other options there are, please see the [VCR docs](https://vcrpy.readthedocs.io/en/latest/index.html).\n\nFor more information on how to use langchain, please see the [langchain docs](https://langchain.readthedocs.io/en/latest/).\n',
    'author': 'Amos Jun-yeung Ng',
    'author_email': 'me@amos.ng',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
