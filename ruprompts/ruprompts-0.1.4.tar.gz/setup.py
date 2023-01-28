# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conf', 'ruprompts', 'ruprompts.cli']

package_data = \
{'': ['*'],
 'conf': ['backbone/*',
          'callbacks/*',
          'dataset/*',
          'model/*',
          'optimizer/*',
          'preprocessing/*',
          'prompt_format/*',
          'prompt_provider/*',
          'scheduler/*',
          'task/*',
          'tokenizer/*',
          'training/*']}

install_requires = \
['torch>=1.10.0,<2.0.0',
 'torchtyping>=0.1.4,<0.2.0',
 'transformers>=4.6.0,<5.0.0',
 'typeguard>=2.13.3,<3.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

extras_require = \
{'hydra': ['hydra-core>=1.1.0,<2.0.0', 'datasets>=1.16.1,<2.0.0']}

entry_points = \
{'console_scripts': ['ruprompts-train = ruprompts.cli.train:hydra_entry']}

setup_kwargs = {
    'name': 'ruprompts',
    'version': '0.1.4',
    'description': 'Fast prompt tuning framework for large language models',
    'long_description': '# ruPrompts\n\n**ruPrompts** is a high-level yet extensible library for fast language model tuning via automatic prompt search, featuring integration with HuggingFace Hub, configuration system powered by Hydra, and command line interface.\n\nPrompt is a text instruction for language model, like\n\n```\nTranslate English to French:\ncat =>\n```\n\nFor some tasks the prompt is obvious, but for some it isn\'t. With **ruPrompts** you can define only the prompt format, like `<P*10>{text}<P*10>`, and train it automatically for any task, if you have a training dataset.\n\nYou can currently use **ruPrompts** for text-to-text tasks, such as summarization, detoxification, style transfer, etc., and for styled text generation, as a special case of text-to-text.\n\n## Features\n\n- **Modular structure** for convenient extensibility\n- **Integration with [HF Transformers](https://huggingface.co/transformers/)**, support for all models with LM head\n- **Integration with [HF Hub](https://huggingface.co/models/)** for sharing and loading pretrained prompts\n- **CLI** and configuration system powered by **[Hydra](https://hydra.cc)**\n- **[Pretrained prompts](https://ai-forever.github.io/ru-prompts/pretrained/)** for **[ruGPT-3](https://huggingface.co/sberbank-ai/rugpt3large_based_on_gpt2)**\n\n## Installation\n\n**ruPrompts** can be installed with `pip`:\n\n```sh\npip install ruprompts[hydra]\n```\n\nSee [Installation](https://ai-forever.github.io/ru-prompts/getting-started/installation) for other installation options.\n\n## Usage\n\nLoading a pretrained prompt for styled text generation:\n\n```py\n>>> import ruprompts\n>>> from transformers import pipeline\n\n>>> ppln_joke = pipeline("text-generation-with-prompt", prompt="konodyuk/prompt_rugpt3large_joke")\n>>> ppln_joke("Говорит кружка ложке")\n[{"generated_text": \'Говорит кружка ложке: "Не бойся, не утонешь!".\'}]\n```\n\nFor text2text tasks:\n\n```py\n>>> ppln_detox = pipeline("text2text-generation-with-prompt", prompt="konodyuk/prompt_rugpt3large_detox_russe")\n>>> ppln_detox("Опять эти тупые дятлы все испортили, чтоб их черти взяли")\n[{"generated_text": \'Опять эти люди все испортили\'}]\n```\n\nProceed to [Quick Start](https://ai-forever.github.io/ru-prompts/getting-started/quick-start) for a more detailed introduction or start using **ruPrompts** right now with our [Colab Tutorials](https://ai-forever.github.io/ru-prompts/tutorials).\n\n## License\n\n**ruPrompts** is Apache 2.0 licensed. See the LICENSE file for details.\n',
    'author': 'Sber AI',
    'author_email': 'nekonodyuk@sberbank.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sberbank-ai.github.io/ru-prompts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
