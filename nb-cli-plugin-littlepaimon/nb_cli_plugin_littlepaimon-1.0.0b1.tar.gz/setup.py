# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_cli_plugin_littlepaimon']

package_data = \
{'': ['*']}

install_requires = \
['nb-cli>=1.0.2,<2.0.0', 'py-cpuinfo>=9.0.0,<10.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'nb': ['paimon = nb_cli_plugin_littlepaimon.plugin:main']}

setup_kwargs = {
    'name': 'nb-cli-plugin-littlepaimon',
    'version': '1.0.0b1',
    'description': 'Nonebot Cli plugin for LittlePaimon',
    'long_description': '<!-- markdownlint-disable MD033 MD041 -->\n<p align="center">\n  <img src="https://cli.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">\n</p>\n\n<div align="center">\n\n# NB CLI Plugin For LittlePaimon\n\n_✨ 为小派蒙Bot定制的 NoneBot2 CLI 插件 ✨_\n\n</div>\n\n## 安装\n\n使用 nb-cli\n\n```shell\nnb self install nb-cli-plugin-littlepaimon\n```\n\n使用 pipx\n\n```shell\npipx inject nb-cli nb-cli-plugin-littlepaimon\n```\n\n## 使用\n\n- `nb paimon` 交互式使用\n  - `nb paimon create` 交互式指引安装[小派蒙](https://github.com/CMHopeSunshine/LittlePaimon)\n  - `nb paimon logo` 展示小派蒙logo\n\n## TODO\n\n- [ ] 更新资源\n- [ ] 修改配置\n- [ ] 安装小派蒙插件\n- [ ] more',
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
