# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cup',
 'cup.net',
 'cup.net.asyn',
 'cup.res',
 'cup.services',
 'cup.shell',
 'cup.storage',
 'cup.util',
 'cup.web']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=3.0.0,<4.0.0',
 'pexpect>=4.8.0,<5.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'cup',
    'version': '3.2.32',
    'description': 'A common useful python library',
    'long_description': '![cuplogo](http://cup.iobusy.com/cup.logo.png)\n\n## Notice \n\n- Visit http://cup.iobusy.com for more details\n    - **访问 http://cup.iobusy.com 获取更多信息**\n- **From now (Version 3.3.1) on, CUP will only support Python3 ** \n    - If you want use cup in Python2.7.x, plz install it with version < 3.3\n        - e.g.  # python -m pip install cup==3.2.31\n        - cup 3.2.X versions will only maintain bug fixes for Python2. Will not add any new features.\n        - If you want to try new features, pls use cup under Python3.\n    - If you use cup under Python3, pls refer to the `Installation` part.\n    - 从 3.3.1 版本开始，Cup 新版本只对 Python3提供支持。如果你想继续在python2.7中使用它，请使用3.2.X版本。\n    - 后续 3.2.X版本对继续提供对Python2.7的bug fix 支持，但不会再增加新的功能。\n    - 推荐大家在Python3中使用Cup\n\n## Quick Start\n### 1. Download\n    - git clone CUP or download the released tar balls\n\n### 2. Installation\n\nInstall from pip\n\n```bash\npip install cup\n```\n\nInstall from source code:\n\n```bash\npython setup.py install\n```\n\n### 3. Doc & Wiki\n\nVisit Wiki to see more details: https://github.com/Baidu/CUP/wiki\n\nVisit Doc site to see py-docs: http://cupdoc.iobusy.com/\n\n```python\n# Examples:\n# 1. Get system info\nimport cup\n# count cpu usage in interval, by default 60 seconds\nfrom cup.res import linux\ncpuinfo = linux.get_cpu_usage(intvl_in_sec=60)\nprint cpuinfo.usr\n\n# total, available, percent, used, free, active, inactive, buffers, cached\nfrom cup.res import linux\nmeminfo = linux.get_meminfo()\nprint meminfo.total\nprint meminfo.available\n```\n\n\n## Tests\n    - Install python-nose before running the tests\n    - run `cd ./cup_tests; nosetests -s`\n\n## Contribute To CUP\n    - Commit code to GITHUB, https://github.com/baidu/CUP\n    - Need to check pep8 and pylint rules before you start a pull request\n\n## Discussion\n    - Github Issues\n\n## Reference\n      * Pexpect http://pexpect.sourceforge.net/ (under MIT license)\n      * Httplib2 http://code.google.com/p/httplib2/ (under MIT license)\n      * requests https://github.com/kennethreitz/requests (under Apache V2 license)\n      * pymysql https://github.com/PyMySQL/PyMySQL (under MIT license)\n\n## WIKI\nhttps://github.com/Baidu/CUP/wiki\n\n## code directory tree:\n\n```text\ncup\n    |-- cache.py                module              Memory cache related module\n    |-- decorators.py           module              Decorators of python\n    |-- err.py                  module              Exception classes for CUP\n    |-- __init__.py             module              Default __init__.py\n    |-- log.py                  module              CUP logging\n    |-- mail.py                 module              CUP Email module (send emails)\n    |-- net                     package             Network operations, such as net handler parameter tuning\n    |-- oper.py                 module              Mixin operations\n    |-- platforms.py            module              Cross-platform operations\n    |-- res                     package             Resource usage queries (in /proc)、Process query、etc\n    |-- shell                   package             Shell Operations、cross-hosts execution\n    |-- services                package             Heartbeat、Threadpool based executors、file service、etc\n    |-- thirdp                  package             Third-party modules： pexpect、httplib2\n    |-- timeplus.py             module              Time related module\n    |-- unittest.py             module              Unittest、assert、noseClass\n    |-- util                    package             ThreadPool、Interruptable-Thread、Rich configuration、etc\n    |-- version.py              module              CUP Version\n```\n\n\n\n## 快速开始\n### 1. 下载\n    - 克隆git代码或者下载已发布的tar包\n\n### 2. 安装\n    - pip 安装  `pip install cup`\n    - 源码安装 `python setup.py install`\n\n### 3. 使用说明\n- Visit Wiki to see more details: https://github.com/Baidu/CUP/wiki\n- Visit Doc site to see py-docs: http://cupdoc.iobusy.com/\n\n举例说明：\n\n```python\n# Examples:\n# 1. Get system info\nimport cup\n# count cpu usage in interval, by default 60 seconds\nfrom cup.res import linux\ncpuinfo = linux.get_cpu_usage(intvl_in_sec=60)\nprint cpuinfo.usr\n\n# total, available, percent, used, free, active, inactive, buffers, cached\nfrom cup.res import linux\nmeminfo = linux.get_meminfo()\nprint meminfo.total\nprint meminfo.available\n```\n\n\n## Tests\n    - Install python-nose before running the tests\n    - run `cd ./cup_tests; nosetests -s`\n\n## 向CUP贡献代码\n直接在github中提交patch就可以了\n    - Commit code to GITHUB, https://github.com/baidu/CUP\n    - Need to check pep8 and pylint rules before you start a pull request\n\n## Discussion\n    - Github Issues\n\n## Reference\n      * Pexpect http://pexpect.sourceforge.net/ (under MIT license)\n      * Httplib2 http://code.google.com/p/httplib2/ (under MIT license)\n      * requests https://github.com/kennethreitz/requests (under Apache V2 license)\n      * pymysql https://github.com/PyMySQL/PyMySQL (under MIT license)\n\n## 代码树结构:\n\n```text\ncup\n    |-- cache.py                module              缓存相关模块 （Memory cache related module）\n    |-- decorators.py           module              python修饰符，比如@Singleton单例模式 (Decorators of python)\n    |-- err.py                  module              异常exception类, Exception classes for CUP\n    |-- __init__.py             module              默认__init__.py, Default __init__.py\n    |-- log.py                  module              打印日志类，CUP的打印日志比较简洁、规范，设置统一、简单(cup logging module)\n    |-- mail.py                 module              发送邮件 （CUP Email module (send emails)）\n    |-- net                     package             网络相关操作（Network operations, such as net handler parameter tuning）\n    |-- oper.py                 module              一些混杂操作(Mixin operations)\n    |-- platforms.py            module              跨平台、平台相关操作函数(Cross-platform operations)\n    |-- res                     package             资源获取、实时用量统计等，所有在/proc可获得的系统资源、进程、设备等信息 （Resource usage queries (in /proc)、Process query、etc）\n    |-- shell                   package             命令Shell操作pakcage（Shell Operations、cross-hosts execution）\n    |-- services                package             构建服务支持的类（比如心跳、线程池based执行器等等）Heartbeat、Threadpool based executors、file service、etc\n    |-- thirdp                  package             第三方依赖纯Py模块（Third-party modules： pexpect、httplib2）\n    |-- timeplus.py             module              时间相关的模块(Time related module)\n    |-- unittest.py             module              单元测试支持模块（Unittest、assert、noseClass）\n    |-- util                    package             线程池、可打断线程、语义丰富的配置文件支持（ThreadPool、Interruptable-Thread、Rich configuration、etc）\n    |-- version.py              module              内部版本文件，CUP Version\n```\n',
    'author': 'CUP Dev Team lead by Guannan Ma',
    'author_email': 'mythmgn@hotmail.com',
    'maintainer': 'Guannan Ma',
    'maintainer_email': 'mythmgn@hotmail.com',
    'url': 'https://github.com/baidu/CUP',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
