# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['VK']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'docstring-parser>=0.15,<0.16',
 'httpx>=0.23.3,<0.24.0',
 'pydantic>=1.10.1,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'vkpybot',
    'version': '0.1.3',
    'description': '',
    'long_description': "VK is library that allows to create chatbots for vk easy and fast\n\n# Quickstart\n\nEasiest hi-bot\n\n    from VK import Bot\n\n\n    bot = Bot(api_token)\n\n    @bot.command('hi')\n    def greet(message):\n        return 'Hi'\n    \n    bot.start()\n\n# Documentation\n\n`Bot` - main class\n\n### Parameters\n\n- `access_token` - string to access api\n- `bot_admin` - id of user, that will gain maximum access for bot`s commands\n- `session` - `GroupSession` object to access api (will be created automatically if not passed)\n- `event_server` - `CallBackServer` or `LongPollServer` that will pass events to bot (LongPollServer will bew created\n  automatically)\n- `log_file` - name of log_file (will bew created at /log directory)\n- `log_level`\n\n## Commands\n\n`Bot.command()` - decorator for the functions that will be converted to a `Command` object\n\n### Parameters\n\n- `name` - the main name of command (by default the name of function)\n- `aliases` - the alternative names of command\n- `access_level` - the minimum [access level](#AccessLevel) of access to run command\n- `message_if_deny` - string, that will be replied to message, if access_level less then `access_level`\n- `use_doc` - weather or not use the documentation of function in auto-generated documentation\n\nCommands can be declared both synchronous and asynchronous\n\n    bot.command()\n    def hi():\n        return 'Hi!'\n\n    bot.command()\n    async def bye():\n        return 'Bye-bye!'\n\nYou can add `message` argument to the command-function to gain access to the message, that called the command\n\n    bot.command()\n    def hi(message):\n        return f'Hi, {message.sender}!'\n\n\n> Framework will automatically use the returned string as text of message to reply and ignore all other returned objects (including None)\n\n\n## AccessLevel\n\nThere are 3 access levels now\n\n1. USER - every user in conversations\n2. ADMIN - admins of conversation and any user in private chat with bot\n3. BOT_ADMIN - user, that was declared as `bot_admin`\n\n## Regex (Experimental)\n\nYou can write functions, that will be automatically called if message matches given pattern\n\n    bot.regex('.*hi.*')\n    async def regex_hi(message):\n        await message.reply('Your message contains hi')\n\n## Message\n\n~~Some description~~\n\n### Fields\n\n- `date`- [time.struct_time](https://docs.python.org/3/library/time.html#time.struct_time) - sending time of message\n- `text` str\n- `chat` - [Chat](#Chat) object, where message was send\n- `sender` - [User](#User) object, who send the message\n\n## Chat\n\n## User",
    'author': 'Vlatterran',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
