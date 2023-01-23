# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_molar_mass']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2[fastapi]>=2.0.0rc3,<3.0.0', 'rply>=0.7.8,<0.8.0']

setup_kwargs = {
    'name': 'nonebot-plugin-molar-mass',
    'version': '0.2.2',
    'description': 'A tool to calculate molar mass for middle school students.',
    'long_description': '# nonebot-plugin-molar-mass\n\n本项目为 `Nonebot2` 插件，用来计算摩尔质量或相对分子质量。\n\n因为我每次遇到计算题都要去翻课本，然后按计算器，不胜其烦，导致了这个库的出现。\n\n可以查看本项目的 `CLI` 分支，直接使用 `cli` 版本。\n\n# 安装\n\n使用 `pip` 安装：\n\n```bash\n> pip install -U nonebot-plugin-molar-mass\n```\n\n使用 `nb-cli` 安装：\n\n```bash\n> nb plugin install nonebot-plugin-molar-mass\n```\n\n# 使用\n\n发送 `/摩尔质量 化学式` 或 `/相对分子质量 化学式` 或 `/mol 化学式`。注意，这里的斜杠指的是 `COMMAND_START`，你可以参考 Nonebot 官方文档配置。\n\n以下为几组输入输出的例子：\n\n```\n> NaOH\n40\n> H2SO4\n98\n> 2HCl\n73\n> (NH4)2SO4\n132\n> CuSO4+5H2O\n250\n```\n',
    'author': 'kifuan',
    'author_email': 'kifuan@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kifuan/nonebot-plugin-molar-mass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
