# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['llm_kira',
 'llm_kira.client',
 'llm_kira.client.llms',
 'llm_kira.client.module',
 'llm_kira.client.module.plugin',
 'llm_kira.client.text_analysis_tools',
 'llm_kira.client.text_analysis_tools.api.keyphrase',
 'llm_kira.client.text_analysis_tools.api.keywords',
 'llm_kira.client.text_analysis_tools.api.sentiment',
 'llm_kira.client.text_analysis_tools.api.summarization',
 'llm_kira.client.text_analysis_tools.api.text_similarity',
 'llm_kira.openai',
 'llm_kira.openai.api',
 'llm_kira.openai.resouce',
 'llm_kira.utils',
 'llm_kira.utils.fatlangdetect',
 'llm_kira.utils.langdetect']

package_data = \
{'': ['*'],
 'llm_kira.client.text_analysis_tools': ['api/data/*'],
 'llm_kira.client.text_analysis_tools.api.sentiment': ['data/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'duckduckgo-search==2.8.0',
 'elara>=0.5.4,<0.6.0',
 'httpx>=0.23.1,<0.24.0',
 'jieba>=0.42.1,<0.43.0',
 'loguru>=0.6.0,<0.7.0',
 'nltk>=3.8,<4.0',
 'numpy>=1.22.1,<2.0.0',
 'openai-async>=0.0.2,<0.0.3',
 'pillow>=9.3.0,<10.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'redis>=4.4.0,<5.0.0',
 'tiktoken>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'llm-kira',
    'version': '0.2.3',
    'description': 'chatbot client for llm',
    'long_description': '# llm-kira\n\nA refactored version of the `openai-kira` specification. Use redis or a file database.\n\nBuilding ChatBot with LLMs.Using `async` requests.\n\n> Contributors welcomed.\n\n## Features\n\n* safely cut context\n* usage\n* async request api / curl\n* multi-Api Key load\n* self-design callback\n\n## Basic Use\n\n`pip install -U llm-kira`\n\n**Init**\n\n```python\nimport llm_kira\n\nllm_kira.setting.redisSetting = llm_kira.setting.RedisConfig(host="localhost",\n                                                             port=6379,\n                                                             db=0,\n                                                             password=None)\nllm_kira.setting.dbFile = "client_memory.db"\nllm_kira.setting.proxyUrl = None  # "127.0.0.1"\n\n# Plugin\nllm_kira.setting.webServerUrlFilter = False\nllm_kira.setting.webServerStopSentence = ["广告", "营销号"]  # 有默认值\n```\n\n## Demo\n\n**More examples of use in `test/test.py`.**\n\nTake `openai` as an example\n\n```python\nimport asyncio\nimport random\nimport llm_kira\nfrom llm_kira.client import Optimizer\nfrom llm_kira.client.types import PromptItem\nfrom llm_kira.client.llms.openai import OpenAiParam\nfrom typing import List\n\nopenaiApiKey = ["key1", "key2"]\nopenaiApiKey: List[str]\n\nreceiver = llm_kira.client\nconversation = receiver.Conversation(\n    start_name="Human:",\n    restart_name="AI:",\n    conversation_id=10093,  # random.randint(1, 10000000),\n)\n\nllm = llm_kira.client.llms.OpenAi(\n    profile=conversation,\n    api_key=openaiApiKey,\n    token_limit=3700,\n    auto_penalty=False,\n    call_func=None,\n)\n\nmem = receiver.MemoryManager(profile=conversation)\nchat_client = receiver.ChatBot(profile=conversation,\n                               memory_manger=mem,\n                               optimizer=Optimizer.SinglePoint,\n                               llm_model=llm)\n\n\nasync def chat():\n    promptManager = receiver.PromptManager(profile=conversation,\n                                         connect_words="\\n",\n                                         template="Templates, custom prefixes"\n                                         )\n    promptManager.insert(item=PromptItem(start=conversation.start_name, text="My id is 1596321"))\n    response = await chat_client.predict(llm_param=OpenAiParam(model_name="text-davinci-003", n=2, best_of=2),\n                                         prompt=promptManager,\n                                         predict_tokens=500,\n                                         increase="External enhancements, or searched result",\n                                         )\n    print(f"id {response.conversation_id}")\n    print(f"ask {response.ask}")\n    print(f"reply {response.reply}")\n    print(f"usage:{response.llm.usage}")\n    print(f"usage:{response.llm.raw}")\n    print(f"---{response.llm.time}---")\n\n    promptManager.clean()\n    promptManager.insert(item=PromptItem(start=conversation.start_name, text="Whats my id？"))\n    response = await chat_client.predict(llm_param=OpenAiParam(model_name="text-davinci-003"),\n                                         prompt=promptManager,\n                                         predict_tokens=500,\n                                         increase="外部增强:每句话后面都要带 “喵”",\n                                         # parse_reply=None\n                                         )\n    _info = "parse_reply 函数回调会处理 llm 的回复字段，比如 list 等，传入list，传出 str 的回复。必须是 str。"\n    _info2 = "The parse_reply function callback handles the reply fields of llm, such as list, etc. Pass in list and pass out str for the reply."\n    print(f"id {response.conversation_id}")\n    print(f"ask {response.ask}")\n    print(f"reply {response.reply}")\n    print(f"usage:{response.llm.usage}")\n    print(f"usage:{response.llm.raw}")\n    print(f"---{response.llm.time}---")\n\n\nasyncio.run(chat())\n```\n\n## Frame\n\n```\n├── client\n│      ├── agent.py  //profile class\n│      ├── anchor.py // client etc.\n│      ├── enhance.py // web search etc.\n│      ├── __init__.py\n│      ├── llm.py // llm func.\n│      ├── module  // plugin for enhance\n│      ├── Optimizer.py // memory Optimizer (cutter\n│      ├── pot.py // test cache\n│      ├── test_module.py // test plugin\n│      ├── text_analysis_tools // nlp support\n│      ├── types.py // data class\n│      └── vocab.json // cache?\n├── __init__.py\n├── openai  // func\n│      ├── api // data\n│      ├── __init__.py\n│      └── resouce  // func\n├── requirements.txt\n└── utils  // utils... tools...\n    ├── chat.py\n    ├── data.py\n    ├── fatlangdetect //lang detect\n    ├── langdetect\n    ├── network.py\n    └── setting.py\n\n```\n',
    'author': 'sudoskys',
    'author_email': 'coldlando@hotmail.com',
    'maintainer': 'sudoskys',
    'maintainer_email': 'coldlando@hotmail.com',
    'url': 'https://github.com/sudoskys/llm_kira',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
