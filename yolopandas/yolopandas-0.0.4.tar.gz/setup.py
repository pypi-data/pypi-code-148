# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yolopandas']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.8.0,<9.0.0',
 'langchain>=0.0.60,<1',
 'openai>=0.26.0,<0.27.0',
 'pandas>=1.4,<2.0']

setup_kwargs = {
    'name': 'yolopandas',
    'version': '0.0.4',
    'description': 'Interact with Pandas objects via LLMs and langchain.',
    'long_description': '# YOLOPandas\n\nInteract with Pandas objects via LLMs and [LangChain](https://github.com/hwchase17/langchain).\n\nYOLOPandas lets you specify commands with natural language and execute them directly on Pandas objects.\nYou can preview the code before executing, or set `yolo=True` to execute the code straight from the LLM.\n\n**Warning**: YOLOPandas will execute arbitrary Python code on the machine it runs on. This is a dangerous thing to do.\n\nhttps://user-images.githubusercontent.com/26529506/214591990-c295a283-b9e6-4775-81e4-28917183ebb1.mp4\n\n## Quick Install\n\n`pip install yolopandas`\n\n## Basic usage\n\nYOLOPandas adds a `llm` accessor to Pandas dataframes.\n\n```python\nfrom yolopandas import pd\n\ndf = pd.DataFrame(\n    [\n        {"name": "The Da Vinci Code", "type": "book", "price": 15, "quantity": 300, "rating": 4},\n        {"name": "Jurassic Park", "type": "book", "price": 12, "quantity": 400, "rating": 4.5},\n        {"name": "Jurassic Park", "type": "film", "price": 8, "quantity": 6, "rating": 5},\n        {"name": "Matilda", "type": "book", "price": 5, "quantity": 80, "rating": 4},\n        {"name": "Clockwork Orange", "type": None, "price": None, "quantity": 20, "rating": 4},\n        {"name": "Walden", "type": None, "price": None, "quantity": 100, "rating": 4.5},\n    ],\n)\n\ndf.llm.query("What item is the least expensive?")\n```\nThe above will generate Pandas code to answer the question, and prompt the user to accept or reject the proposed code.\nAccepting it in this case will return a Pandas dataframe containing the result.\n\nAlternatively, you can execute the LLM output without first previewing it:\n```python\ndf.llm.query("What item is the least expensive?", yolo=True)\n```\n\n`.query` can return the result of the computation, which we do not constrain. For instance, while `"Show me products under $10"` will return a dataframe, the query `"Split the dataframe into two, 1/3 in one, 2/3 in the other. Return (df1, df2)"` can return a tuple of two dataframes. You can also chain queries together, for instance:\n```python\ndf.llm.query("Group by type and take the mean of all numeric columns.", yolo=True).llm.query("Make a bar plot of the result and use a log scale.", yolo=True)\n```\n\nSee the [example notebook](docs/example_notebooks/example.ipynb) for more ideas.\n\n\n## LangChain Components\n\nThis package uses several LangChain components, making it easy to work with if you are familiar with LangChain. In particular, it utilizes the LLM, Chain, and Memory abstractions.\n\n### LLM Abstraction\n\nBy working with LangChain\'s LLM abstraction, it is very easy to plug-and-play different LLM providers into YOLOPandas. You can do this in a few different ways:\n\n1. You can change the default LLM by specifying a config path using the `LLPANDAS_LLM_CONFIGURATION` environment variable. The file at this path should be in [one of the accepted formats](https://langchain.readthedocs.io/en/latest/modules/llms/examples/llm_serialization.html).\n\n2. If you have a LangChain LLM wrapper in memory, you can set it as the default LLM to use by doing:\n\n```python\nimport yolopandas\nyolopandas.set_llm(llm)\n```\n\n3. You can set the LLM wrapper to use for a specific dataframe by doing: `df.reset_chain(llm=llm)`\n\n\n### Chain Abstraction\n\nBy working with LangChain\'s Chain abstraction, it is very easy to plug-and-play different chains into YOLOPandas. This can be useful if you want to customize the prompt, customize the chain, or anything like that.\n\nTo use a custom chain for a particular dataframe, you can do:\n\n```python\ndf.set_chain(chain)\n```\n\nIf you ever want to reset the chain to the base chain, you can do:\n\n```python\ndf.reset_chain()\n```\n\n### Memory Abstraction\n\nThe default chain used by YOLOPandas utilizes the LangChain concept of [memory](https://langchain.readthedocs.io/en/latest/modules/memory.html). This allows for "remembering" of previous commands, making it possible to ask follow up questions or ask for execution of commands that stem from previous interactions.\n\nFor example, the query `"Make a seaborn plot of price grouped by type"` can be followed with `"Can you use a dark theme, and pastel colors?"` upon viewing the initial result.\n\nBy default, memory is turned on. In order to have it turned off by default, you can set the environment variable `LLPANDAS_USE_MEMORY=False`.\n\nIf you are resetting the chain, you can also specify whether to use memory there:\n\n```python\ndf.reset_chain(use_memory=False)\n```\n\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/ccurme/yolopandas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
