# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_memes']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-imageutils>=0.1.13,<0.2.0',
 'nonebot2[fastapi]>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-memes',
    'version': '0.3.10',
    'description': 'Nonebot2 plugin for making memes',
    'long_description': '<div align="center">\n\n  <a href="https://v2.nonebot.dev/">\n    <img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">\n  </a>\n\n# nonebot-plugin-memes\n\n_✨ [Nonebot2](https://github.com/nonebot/nonebot2) 插件，用于文字类表情包制作 ✨_\n\n<p align="center">\n  <img src="https://img.shields.io/github/license/noneplugin/nonebot-plugin-memes" alt="license">\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">\n  <img src="https://img.shields.io/badge/nonebot-2.0.0b4+-red.svg" alt="NoneBot">\n  <a href="https://pypi.org/project/nonebot-plugin-memes">\n    <img src="https://badgen.net/pypi/v/nonebot-plugin-memes" alt="pypi">\n  </a>\n  <a href="https://jq.qq.com/?_wv=1027&k=wDVNrMdr">\n    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-682145034-orange" alt="qq group">\n  </a>\n</p>\n\n</div>\n\n\n头像相关表情包制作：[nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet)\n\n\n### ！！！注意\n\n- 为避免表情开关的命令与“头像表情包”插件冲突，同时更准确地描述插件功能，本插件由“表情包制作”更名为“文字表情包”，相应的指令也做了调整\n\n- 为避免误触发，大多数表情改为需要在指令后加空格，如：“鲁迅说 我没说过这句话”\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_memes\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_memes\n```\n\n#### 字体和资源\n\n插件使用 [nonebot-plugin-imageutils](https://github.com/noneplugin/nonebot-plugin-imageutils) 插件来绘制文字，字体配置可参考该插件的说明\n\n插件在启动时会检查并下载图片资源，初次使用时需等待资源下载完成\n\n可以手动下载 `resources` 下的 `images` 和 `thumbs` 文件夹，放置于机器人运行目录下的 `data/memes/` 文件夹中\n\n可以手动下载 `resources` 下 `fonts` 中的字体文件，放置于 nonebot-plugin-imageutils 定义的字体路径，默认为机器人运行目录下的 `data/fonts/` 文件夹\n\n\n### 配置项\n\n> 以下配置项可在 `.env.*` 文件中设置，具体参考 [NoneBot 配置方式](https://v2.nonebot.dev/docs/tutorial/configuration#%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F)\n\n#### `memes_command_start`\n - 类型：`List[str]`\n - 默认：`[""]`\n - 说明：命令起始标记，默认包含空字符串\n\n#### `memes_resource_url`\n - 类型：`str`\n - 默认：`https://ghproxy.com/https://raw.githubusercontent.com/noneplugin/nonebot-plugin-memes/v0.3.x/resources`\n - 说明：资源下载链接，默认为使用`ghproxy`代理的github仓库链接\n\n#### `memes_disabled_list`\n - 类型：`List[str]`\n - 默认：`[]`\n - 说明：禁用的表情包列表，需填写表情名称的列表，表情名称可以在`data_source.py`文件中查看。若只是临时关闭，可以用下文中的“表情包开关”\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n支持的表情包：\n\n发送“文字表情包”显示下图的列表：\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/11/29/496PAMb25GgTuyq.jpg" width="500" />\n</div>\n\n\n#### 表情包开关\n\n群主 / 管理员 / 超级用户 可以启用或禁用某些表情包\n\n发送 `启用文字表情/禁用文字表情 [表情名]`，如：`禁用文字表情 鲁迅说`\n\n超级用户 可以设置某个表情包的管控模式（黑名单/白名单）\n\n发送 `全局启用文字表情 [表情名]` 可将表情设为黑名单模式；\n\n发送 `全局禁用文字表情 [表情名]` 可将表情设为白名单模式；\n\n\n### 示例\n\n - `/鲁迅说 我没说过这句话`\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/06/12/dqRF8egWb3U6Vfz.png" width="250" />\n</div>\n\n\n - `/举牌 aya大佬带带我`\n\n<div align="left">\n  <img src="https://s2.loli.net/2022/06/12/FPuBosEgM3Qh1rJ.jpg" width="250" />\n</div>\n\n\n### 特别感谢\n\n- [Ailitonia/omega-miya](https://github.com/Ailitonia/omega-miya) 基于nonebot2的qq机器人\n\n- [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) 基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库，非常可爱的绪山真寻bot\n\n- [kexue-z/nonebot-plugin-nokia](https://github.com/kexue-z/nonebot-plugin-nokia) 诺基亚手机图生成\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/noneplugin/nonebot-plugin-memes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
