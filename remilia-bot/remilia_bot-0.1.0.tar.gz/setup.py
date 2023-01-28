# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remilia',
 'remilia.src',
 'remilia.src.plugins.Gua64',
 'remilia.src.plugins.block',
 'remilia.src.plugins.chat',
 'remilia.src.plugins.cmd',
 'remilia.src.plugins.code_runner',
 'remilia.src.plugins.pix',
 'remilia.src.plugins.setu',
 'remilia.src.plugins.start',
 'remilia.src.plugins.status']

package_data = \
{'': ['*'], 'remilia.src.plugins.chat': ['resource/*']}

install_requires = \
['apscheduler>=3.9.1.post1',
 'loguru>=0.6.0',
 'psutil>=5.9.0',
 'python-telegram-bot>=20.0',
 'pyyaml>=6.0']

setup_kwargs = {
    'name': 'remilia-bot',
    'version': '0.1.0',
    'description': '女生自用(?)电报机器人',
    'long_description': '# RemiliaBot\n女生自用(?)电报机器人\n\n### 使用方法\n\n1. 安装Python3并配置好环境变量\n2. 创建一个空文件夹, 在命令行cd到该文件夹下\n3. 输入以下命令安装并运行\n\n```sh\npip install remilia-bot   # 从 PyPI 安装 Bot\npython -m remilia   # 运行 Bot\n```\n',
    'author': '月ヶ瀬',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tkgs0/RemiliaBot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
