# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['qq',
 'qq.plugins',
 'qq.plugins.celery',
 'qq.plugins.sqlalchemy',
 'qq.plugins.sqlalchemy.tests',
 'qq.plugins.tests',
 'qq.plugins.tornado',
 'qq.tests']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0']

extras_require = \
{'alembic': ['alembic>=1.0.9,<2.0.0'],
 'celery': ['celery>=5.2.2'],
 'developer': ['alembic>=1.0.9,<2.0.0',
               'sqlalchemy>=1.3.3,<2.0.0',
               'redis>=3.2.1,<4.0.0',
               'celery>=5.2.2'],
 'redis': ['redis>=3.2.1,<4.0.0'],
 'sqlalchemy': ['sqlalchemy>=1.3.3,<2.0.0']}

setup_kwargs = {
    'name': 'quackquack',
    'version': '1.2.0',
    'description': 'Quack Quack: A simple application framework',
    'long_description': 'About\n=====\n\n`Documentation <https://qqpy.org/>`_\n\n\nOverview\n--------\n\nThis project aims to resolve problem of configuring an application, which needs to\nhave initialization step (for example: for gathering settings or establishing\nconnections) and use Python style code (context managers and decorators) with\ndependency injection to get those data.\n\nFor example, normally you would need to use two separate mechanism for connection\nto the database (one for web, and one for celery). Mostly it uses the web framework\nconfiguration, to use in the celery code. It is fine, until a third sub-application\narrives. Or you have many microservices, where web frameworks are different\ndepending on the microservice purpose.\n\nSecond goal was to make synchronized code without any globals or magic. That is\nwhy using Quack Quack you know when the application is initialized (started),\nor where to look for code you are using.\n\nIn order to use QQ, you don\'t need to use hacks in some starting files, like\nimporting something from django, starting the application, and the import the\nrest.\n\nQuick Using Example\n-------------------\n\nTo use Quack Quack you need to create the application class (inherited from\n``qq.Application``\\ ) in which you need to add plugins. After configuring, you\nneed to "start" (initialize)\nthe application. After that you can use the application as context manager.\nAlso, you can make simple decorator, so you can use injectors (dependency\ninjection) in function\'s arguments.\n\n.. code-block:: python\n\n    from qq import Application\n    from qq import ApplicationInitializer\n    from qq import Context\n    from qq import SimpleInjector\n    from qq.plugins import SettingsPlugin\n    from qq.plugins.types import Settings\n\n\n    class MyApplication(Application):\n        def create_plugins(self):\n            self.plugins["settings"] = SettingsPlugin("settings")\n\n\n    application = MyApplication()\n    application.start("application")\n\n    with Context(application) as ctx:\n        print(ctx["settings"])\n\n    app = ApplicationInitializer(application)\n\n\n    @app\n    def samplefun(settings: Settings = SimpleInjector("settings")):\n        print(settings)\n\n\n    samplefun()\n    samplefun({"info": "fake settings"})  # dependency injection !!\n\n\n``context["settings"]`` in above example, is a variable made by the SettingsPlugin.\nIf you would like to know more, please go to the `Tutorial <docs/tutorial.md>`_\n\nInstallation\n------------\n\n.. code-block:: bash\n\n   pip install quackquack\n',
    'author': 'Dominik Dlugajczyk',
    'author_email': 'msocek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/socek/quackquack',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
