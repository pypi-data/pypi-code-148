# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['ayaka_prevent_bad_words']
install_requires = \
['ayaka>=0.0.2.0,<0.0.4.0', 'nonebot-adapter-onebot>=2.1.5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-prevent-bad-words',
    'version': '0.4.1',
    'description': '坏词撤回',
    'long_description': '# 坏词撤回 0.4.1\n\n基于[ayaka](https://github.com/bridgeL/ayaka)开发的 坏词撤回 插件\n\n任何问题请发issue\n\n- 自动撤回包含屏蔽词的消息\n- 只适用于群聊\n- 管理员无法撤回其他管理员和群主的发言\n\n## 安装插件\n\n`nb plugin install nonebot-plugin-ayaka-prevent-bad-words`\n\n## 配置\n\n文件位置：`data/ayaka/坏词撤回.json`（该文件在第一次启动时会自动生成）\n\n### word_packages\n\n敏感词列表，可设置若干个词包，供各群组独立使用或交叉使用\n\n```json\n{\n\t"word_packages":[\n\t\t{\n\t\t\t"name": "违禁词包1",\n\t\t\t"words":  ["词1","词2"],\n\t\t\t"groups": [123455667, 102882912]\n\t\t},\n\t\t{\n\t\t\t"name": "违禁词包2",\n\t\t\t"words":  ["词3"],\n\t\t\t"groups": [102882912]\n\t\t}\n\t]\n}\n```\n\n每个词包的`name`属性可以为空\n\n**特殊情况**：若设置群号为0，则该词包会对所有群聊生效\n\n```json\n{\n\t"word_packages":[\n\t\t{\n\t\t\t"name": "违禁词包3",\n\t\t\t"words":  ["词5","词6"],\n\t\t\t"groups": [0]\n\t\t}\n\t]\n}\n```\n\n### delay\n\n延迟n秒后撤回，默认为0\n\n可能会因为网络延迟而不准确\n\n### powerful \n\n检测力度，默认为0\n\n| powerful | 效果                               |\n| -------- | ---------------------------------- |\n| -1       | 发出提示语，不撤回                 |\n| 0        | 只有坏词完全匹配时，才会撤回       |\n| 1        | 即使坏词中夹杂了标点符号，也会撤回 |\n\n### tip \n\n撤回消息后发送提示语，默认为 `请谨言慎行`\n\n若设置为空，则撤回时不发送提示语\n\n## 重启bot\n\n注意：修改配置后，需要重启bot才能生效\n\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-prevent-bad-words',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
