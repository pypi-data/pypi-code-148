# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langchain_visualizer',
 'langchain_visualizer.agents',
 'langchain_visualizer.chains',
 'langchain_visualizer.llms',
 'langchain_visualizer.prompts']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.66,<0.0.67', 'ought-ice>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'langchain-visualizer',
    'version': '0.0.1',
    'description': 'Visualization and debugging tool for LangChain workflows',
    'long_description': '# LangChain Visualizer\n\nAdapts [ICE](https://github.com/oughtinc/ice) for use with [LangChain](https://github.com/hwchase17/langchain) so that you can view LangChain interactions with a beautiful UI.\n\n![Screenshot of an execution run](screenshots/serp_screenshot.png "SERP agent demonstration")\n\nYou can now\n\n- See the full prompt text being sent with every interaction with the LLM\n- Tell from the coloring which parts of the prompt are hardcoded and which parts are templated substitutions\n- Inspect the execution flow and observe when each function goes up the stack\n\n### Running the example screenshot\n\nTo run the example you see in the screenshot, first install this library and optional dependencies:\n\n```bash\npip install langchain-visualizer google-search-results openai\n```\n\nIf you haven\'t yet [set up your OpenAI API keys](https://openai.com/api/), do so now. Then run the following script (adapted from [LangChain docs](https://langchain.readthedocs.io/en/latest/modules/agents/getting_started.html)):\n\n```python\nimport langchain_visualizer\nimport asyncio\nfrom langchain.agents import initialize_agent, load_tools\nfrom langchain.llms import OpenAI\n\nllm = OpenAI(temperature=0.7)\ntools = load_tools(["serpapi", "llm-math"], llm=llm)\nagent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)\nasync def search_agent_demo():\n    return agent.run(\n        "Who is Olivia Wilde\'s boyfriend? What is his current age raised to the 0.23 "\n        "power?"\n    )\n\nlangchain_visualizer.visualize(search_agent_demo)\n```\n\nA browser window will open up, and you can actually see the agent execute happen in real-time!\n\n**Please note that there is a lot of langchain functionality that I haven\'t gotten around to hijacking for visualization.** If there\'s anything you need to show up in the execution trace, please open a PR or issue.\n\n## My other projects\n\nPlease check out [VCR LangChain](https://github.com/amosjyng/vcr-langchain), a library that lets you record LLM interactions for your tests and demos!\n',
    'author': 'Amos Jun-yeung Ng',
    'author_email': 'me@amos.ng',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
