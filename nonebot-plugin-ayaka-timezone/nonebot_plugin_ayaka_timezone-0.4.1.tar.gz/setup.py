# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['ayaka_timezone']
install_requires = \
['ayaka>=0.0.2.0,<0.0.4.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-timezone',
    'version': '0.4.1',
    'description': '时区助手',
    'long_description': '# 时区助手 0.4.1\n\n基于[ayaka](https://github.com/bridgeL/ayaka)开发的 时区助手 插件\n\n任何问题请发issue\n\n注意：只适用于群聊！\n\n## 安装插件\n\n`nb plugin install nonebot-plugin-ayaka-timezone`\n\n# 指令\n| 指令    | 参数           | 功能                                                                      |\n| ------- | -------------- | ------------------------------------------------------------------------- |\n| tz_add  | name, timezone | 添加一条时区转换，例如，#tz_add 北京 8，#tz_add 伦敦 0，#tz_add 洛杉矶 -8 |\n| tz      | name           | 返回name对应时区的时间，例如 #tz 北京                                     |\n| tz      | number         | 返回对应时区的时间，例如 #tz 8                                            |\n| tz_list | 无             | 查看所有的时区转换                                                        |\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-timezone',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
