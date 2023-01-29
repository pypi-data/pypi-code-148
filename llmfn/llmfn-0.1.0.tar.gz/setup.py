# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['llmfn']
install_requires = \
['openai>=0.26.4,<0.27.0']

setup_kwargs = {
    'name': 'llmfn',
    'version': '0.1.0',
    'description': '',
    'long_description': '# llmfn\n\n**llmfn** is a Python library to approximate a function using OpenAI\'s API. You can use it to easily train a language model to approximate your own functions with few-shot prompting.\n\n## Installation\n\nYou can install the package from pip:\n\n```\npip install llmfn\n```\n\n## Usage\n\nFirst, you need to set your OpenAI API key:\n\n```python\nimport os\nimport openai\n\nopenai.api_key = os.getenv("OPENAI_API_KEY")\n```\n\nThen, you can define a list of examples of the function\'s behavior:\n\n```python\nfrom llmfn import Arguments\nfrom llmfn import FunctionExample\n\nexamples = [\n    FunctionExample(arguments=Arguments.call(2, 3), output=5),\n    FunctionExample(arguments=Arguments.call(5, 7), output=12),\n    # ...\n]\n```\n\nFinally, you can use the llmfn decorator to create an approximated version of your function:\n\n```python\nfrom llmfn import llmfn\n\n@llmfn(examples=examples, function_name="my_function")\ndef my_function(a: int, b: int) -> int:\n    return a + b\n\nassert my_function(2, 3) == 5\n```\n\nAlternatively, you can use the `make_llmfn` function to create an approximated version of your function without using the decorator:\n\n```python\nfrom llmfn import make_llmfn\n\nblackbox = make_llmfn(examples=examples, function_name="my_function")\n\nassert blackbox(2, 3) == 5\n```\n\n## Advanced Usage\n\n### Changing the Decoder\n\nBy default, the decoder is set to `lambda x: x`, which simply returns the output as a string. You can change the decoder to parse the output into a different data type:\n\n```python\nfrom llmfn import make_llmfn\n\ndef decoder(output: str) -> int:\n    return int(output)\n\nblackbox = make_llmfn(examples=examples, function_name="my_function", decoder=decoder)\n\nassert blackbox(2, 3) == 5\n```\n\nThe most useful decoder (and the most dangerous) is `eval`, which will evaluate the output as Python code:\n\n```python\nfrom llmfn import make_llmfn\n\nblackbox = make_llmfn(examples=examples, function_name="my_function", decoder=eval)\n\nassert blackbox(2, 3) == 5\n```\n\nUse this with caution - it could be used to execute arbitrary code. (This is why it\'s not the default decoder.)\n\n### Changing the Engine\n\nBy default, the engine is set to `text-davinci-003`. You can change the engine to a different OpenAI engine:\n\n```python\nfrom llmfn import make_llmfn\n\nblackbox = make_llmfn(examples=examples, function_name="my_function", engine="text-curie-001")\n\nassert blackbox(2, 3) == 5\n```\n\n## Limitations\n\n- The function\'s output must be a string.\n- The approximated function can only handle arguments that are compatible with the examples.\n- The approximated function may not work with complex or large functions.\n- The API usage may be subject to rate limits and other restrictions imposed by OpenAI.\n\n## Contributing\n\nWe welcome contributions to this project. If you have any ideas or suggestions, please open an issue or submit a pull request.\n\n## License\n\nThis project is licensed under the MIT License.',
    'author': 'IsaacBreen',
    'author_email': 'mail@isaacbreen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
