# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['criminal_dance', 'criminal_dance.cards']

package_data = \
{'': ['*']}

install_requires = \
['ayaka>=0.0.2.0,<0.0.4.0']

setup_kwargs = {
    'name': 'criminal-dance',
    'version': '0.1.1',
    'description': '犯人在跳舞',
    'long_description': '<div align="center">\n\n# 犯人在跳舞 0.1.1\n\n祝各位新年快乐~\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/criminal_dance)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/criminal_dance)\n![PyPI - License](https://img.shields.io/pypi/l/criminal_dance)\n![PyPI](https://img.shields.io/pypi/v/criminal_dance)\n\n基于ayaka的文字版桌游！\n\n</div>\n\n得益于[ayaka](https://github.com/bridgeL/ayaka)，本插件可作为如下机器人框架的插件使用\n\n- [nonebot2](https://github.com/nonebot/nonebot2)(使用[onebot11](https://github.com/nonebot/adapter-onebot)适配器，可兼容qq频道)\n- [hoshino](https://github.com/Ice-Cirno/HoshinoBot)\n- [nonebot1](https://github.com/nonebot/nonebot)\n\n也可将其作为console程序离线运行\n\n## 安装\n\n```\npip install criminal_dance\n```\n\n## 作为console程序离线运行\n\n```py\n# run.py\nimport ayaka.adapters as cat\nimport criminal_dance\nif __name__ == "__main__":\n    cat.run()\n```\n\n```\npython run.py\n```\n\n## 帮助\n\n```\n[犯人在跳舞]\n3-8人游玩，游玩前请先加bot好友，否则无法发牌\n开局4张手牌，轮流出牌，具体帮助请查看 详细帮助、卡牌帮助、牌库规则\n若长时间不出牌则会被系统强制弃牌（防止挂机）\n- 犯人在跳舞 唤醒猫猫\n[*]\n- 卡牌帮助 <卡牌名> 获取相应的帮助\n- 详细帮助\n- 牌库规则\n- 退出游戏\n- 局势 查看场面局势\n- 手牌 私聊展示手牌\n- 绑定私聊 频道用户请使用该命令\n[room]\n- 加入\n- 离开\n- 房间\n- 开始游戏\n```\n\n### 使用流程\n\n- 发送`犯人在跳舞`启动猫猫，创建游戏房间，发起者自动位于1号位\n- 随后其他人发送`加入`，根据加入顺序确定座次\n- 人数满足要求后，发送`开始`开始游戏，bot将通过私聊告知手牌\n- 之后在群里发送卡牌名称即可打出此卡！\n- 发送`退出游戏`关闭猫猫！\n\n### 卡牌帮助\n\n```\n[第一发现人] 一切都是由您开始。打出时没有特别效果\n[共犯] 打出这张牌成为共犯。当犯人获胜时，您也获得胜利。当犯人输掉游戏时，您也跟着输掉游戏\n[犯人] 您是犯人，不能让其他玩家知道。您只能在只剩下这张手牌时才能打出这张牌，如果您要这么做，您获胜\n[不在场证明] 只要有了这个，您就不是犯人了。打出时没有特别效果。如果您有犯人和不在场证明，侦探质疑时您可以否认\n[侦探] 您的手牌<=2才能打出这张牌。打出时质疑另一位玩家，如果该玩家持有犯人，您获胜\n[普通人] 打出时没有特别效果\n[谣言] 所有玩家随机抽一张他下家玩家的手牌\n[情报交换] 所有玩家把一张牌传给他上家玩家\n[目击者] 看另一个玩家的手牌\n[交易] 和至少还有1张手牌的玩家交换一张手牌。如果这是您打出的最后一张牌，则没有特别效果\n[神犬] 选择一个玩家。该玩家弃掉他其中的一张手牌，并且获得神犬。如果他弃掉一张犯人牌，您获胜\n[警部] 手牌<=2时，选定一个玩家放置此牌，若其最终打出犯人牌，您获得游戏胜利\n```\n\n### 详细帮助\n\n```\n开局每人4张手牌，轮流出牌\n拥有第一发现人的人优先出牌（类似扑克规则的红桃3），且第一张牌必须是第一发现人\n\n犯人牌只有在手牌数为1的时候才能打出，此时打出者作为犯人而胜利\n其他人的目标就是在犯人逃跑成功之前，通过侦探、神犬、警部等牌抓到犯人，此时好人阵营胜利\n\n当你打出共犯牌后，你便加入了坏人阵营，需要协助犯人获胜\n当然，你也可以当个二五仔，若共犯使用侦探等牌抓到了犯人，那么他也视为好人阵营一同胜利\n\n根据参与人数的不同，牌库的牌也不同，具体规则请发送 牌库规则 进一步了解\n\n此外，当游戏进行中时，还可以\n在群聊发送"局势"命令，获得游戏进行情况等信息\n私聊bot发送"手牌"命令，获得你当前的手牌情况\n```\n\n### 牌库规则\n\n```\n3人局，必须有第一发现人、犯人、侦探、不在场证明，加其他任意8张牌\n4人局，必须有第一发现人、犯人、侦探、不在场证明、共犯，加其他任意11张牌\n5人局，必须有第一发现人、犯人、侦探、不在场证明*2、共犯，加其他任意14张牌\n6人局，必须有第一发现人、犯人、侦探*2、不在场证明*2、共犯*2，加其他任意16张牌\n7人局，必须有第一发现人、犯人、侦探*2、不在场证明*3、共犯*2，加其他任意19张牌\n8人局，加全部\n```\n\n## 配置\n\n`data/ayaka/犯人在跳舞.json`\n\n| 属性           | 意义                                                                              |\n| -------------- | --------------------------------------------------------------------------------- |\n| overtime       | 超时限制，超时后系统会自动出牌，防止挂机                                          |\n| auto_card_help | 自动卡牌帮助，每打出一张牌后bot都会发送帮助，等参与玩家熟悉规则后，可以关闭该配置 |\n| rename         | 重命名卡牌，为担心和谐的人准备                                                    |\n\n你可以将犯人改名为大老鼠，共犯改成小老鼠，侦探改成猫猫，警部改成捕鼠笼，谣言改成幸运大转盘，例如：\n\n```json\n{\n    "第一发现人": "第一发现人",\n    "犯人": "大老鼠",\n    "神犬": "神犬",\n    "警部": "捕鼠笼",\n    "共犯": "小老鼠",\n    "普通人": "普通人",\n    "不在场证明": "不在场证明",\n    "目击者": "目击者",\n    "侦探": "猫猫",\n    "谣言": "幸运大转盘",\n    "交易": "交易",\n    "情报交换": "情报交换"\n}\n```\n\n此时，游戏的启动命令将变成 `大老鼠在跳舞`\n\n## 更新记录\n\n### 0.0.1b2\n\n- 原型阶段，勉强可玩\n\n### 0.0.1 \n\n- 重构代码，第一个正式版本，全部功能已实现\n\n### 0.0.2 \n\n- 修复BUG：在交易、情报交换等特殊阶段，无法查询手牌、局势\n\n### 0.0.3\n\n- 重构代码，更精简的逻辑结构\n- 修复BUG：在关闭猫猫后依旧可以通过私聊控制群聊的猫猫\n- 更新依赖 ayaka 0.0.1.4\n\n### 0.0.4b0\n\n- 更新退出游戏命令\n- 修复BUG：使用强制退出时无法关闭超时机制，请使用退出游戏命令\n- 更新依赖 ayaka 0.0.1.5b1\n\n### 0.1.0\n\n- 修复BUG：结束游戏后超时机制没有正确关闭\n- 修复BUG：神犬、侦探牌打出后没有按预期切换牌权\n- 更新依赖 ayaka 0.0.2.0\n\n### 0.1.1\n\n- 更新依赖 ayaka 0.0.3.0\n- 新特性：支持qq频道\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/criminal_dance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
