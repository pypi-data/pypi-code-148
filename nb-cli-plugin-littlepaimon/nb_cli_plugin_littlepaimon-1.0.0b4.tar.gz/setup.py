# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_cli_plugin_littlepaimon',
 'nb_cli_plugin_littlepaimon.commands',
 'nb_cli_plugin_littlepaimon.handlers']

package_data = \
{'': ['*']}

install_requires = \
['nb-cli>=1.0.2,<2.0.0', 'py-cpuinfo>=9.0.0,<10.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'nb': ['paimon = nb_cli_plugin_littlepaimon.plugin:main']}

setup_kwargs = {
    'name': 'nb-cli-plugin-littlepaimon',
    'version': '1.0.0b4',
    'description': 'Nonebot Cli plugin for LittlePaimon',
    'long_description': '<!-- markdownlint-disable MD033 MD041 -->\n<p align="center">\n  <img src="https://cli.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">\n</p>\n\n<div align="center">\n\n# NB CLI Plugin For LittlePaimon\n\n_✨ 为[小派蒙Bot](https://github.com/CMHopeSunshine/LittlePaimon)定制的 NoneBot2 CLI 插件 ✨_\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/CMHopeSunshine/nb-cli-plugin-littlepaimon.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nb-cli-plugin-littlepaimon">\n    <img src="https://img.shields.io/pypi/v/nb-cli-plugin-littlepaimon.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n\n\n</div>\n\n## 安装\n\n<details>\n<summary>安装nb-cli</summary>\n\n> 请确保你的Python版本为3.8+，且在环境变量中\n\n<details>\n<summary>通过 pipx 安装</summary>\n\n```shell\npip install --user pipx\npipx ensurepath\npipx install nb-cli\n```\n</details>\n\n<details>\n<summary>通过 pip 安装</summary>\n\n```shell\npip install nb-cli\n```\n</details>\n\n</details>\n\n<details>\n<summary>安装本插件</summary>\n\n<details>\n<summary>通过 nb-cli 安装</summary>\n\n```shell\nnb self install nb-cli-plugin-littlepaimon\n```\n\n</details>\n\n<details>\n<summary>通过 pipx 安装</summary>\n\n```shell\npipx inject nb-cli nb-cli-plugin-littlepaimon\n```\n</details>\n\n<details>\n<summary>通过 pip 安装</summary>\n\n```shell\npip install nb-cli-plugin-littlepaimon\n```\n</details>\n\n</details>\n\n<details>\n<summary>安装Git</summary>\n\n~~能上Github的话，应该都会装Git吧)~~\n\n</details>\n\n## 使用\n\n- `nb paimon` 交互式使用\n  - `nb paimon create` \n    - 交互式指引安装[LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon)\n    - 自动克隆源码、创建虚拟环境、安装依赖，下载并配置go-cqhttp\n  - `nb paimon install` 安装依赖库到小派蒙环境中\n  - `nb paimon res` 下载或更新小派蒙的资源\n  - `nb paimon logo` 展示小派蒙的logo\n\n## TODO\n\n- [x] 更新资源\n- [ ] 自动安装git\n- [ ] 修改配置\n- [ ] 安装小派蒙插件\n- [ ] more\n\n## 相关项目\n- [nb-cli](https://github.com/nonebot/nb-cli)\n- [LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon)',
    'author': 'CMHopeSunshine',
    'author_email': '277073121@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CMHopeSunshine/nb-cli-plugin-littlepaimon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
