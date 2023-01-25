# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notifypy', 'notifypy.os_notifiers']

package_data = \
{'': ['*'],
 'notifypy.os_notifiers': ['binaries/Notificator.app/Contents/*',
                           'binaries/Notificator.app/Contents/MacOS/*',
                           'binaries/Notificator.app/Contents/Resources/*',
                           'binaries/Notificator.app/Contents/Resources/Scripts/*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

extras_require = \
{':sys_platform == "linux"': ['jeepney']}

entry_points = \
{'console_scripts': ['notifypy = notifypy.cli:entry']}

setup_kwargs = {
    'name': 'notify-py',
    'version': '0.3.41',
    'description': 'Cross-platform desktop notification library for Python',
    'long_description': '<div align="center">\n<br>\n  <h1> notify.py </h1>\n  <i> Cross platform desktop notifications for Python scripts and applications.</i>\n  <br>\n  <br>\n  <p align="center">\n    <img src="https://github.com/ms7m/notify-py/workflows/Test%20Linux/badge.svg">\n    <img src="https://github.com/ms7m/notify-py/workflows/Test%20macOS/badge.svg">\n    <img src="https://github.com/ms7m/notify-py/workflows/Test%20Windows/badge.svg">\n  </p>\n  <br>\n  <p align="center">\n    <img src="https://img.shields.io/badge/Available-on%20PyPi-blue?logoColor=white&logo=Python">\n    <img src="https://img.shields.io/badge/Python-3.6%2B-blue?logo=python">\n    <img src="https://img.shields.io/badge/Formatting-Black-black.svg">\n  </p>\n    <p align="center">\n      <img src="./docs/site/img/demopics.png">\n    <h1>\n  </p>\n</div>\n\n## Docs\n\nYou can read the docs on this Git\'s Wiki, or [here](https://ms7m.github.io/notify-py/)\n\n## Supported Platforms.\n\n- Windows 10/11\n- macOS 10 >=10.10\n- Linux (libnotify)\n\nNo dependencies are required other than loguru & jeepney (Only for linux/DBUS).\n\n---\n\n## Install\n\n```\npip install notify-py\n```\n\n---\n\n## Usage\n\n**Send Simple Notification**\n\n```python\n\nfrom notifypy import Notify\n\nnotification = Notify()\nnotification.title = "Cool Title"\nnotification.message = "Even cooler message."\nnotification.send()\n```\n\n**Send Notification With Icon**\n\n```python\n\nfrom notifypy import Notify\n\nnotification = Notify()\nnotification.title = "Cool Title"\nnotification.message = "Even cooler message."\nnotification.icon = "path/to/icon.png"\n\nnotification.send()\n```\n\n**Send Notification With Sound**\n\n```python\n\nfrom notifypy import Notify\n\nnotification = Notify()\nnotification.title = "Cool Title"\nnotification.message = "Even cooler message."\nnotification.audio = "path/to/audio/file.wav"\n\nnotification.send()\n\n```\n\n**Sending Notifications without blocking**\n\n```python\n\nfrom notifypy import Notify\n\nnotification = Notify()\nnotification.send(block=False)\n\n```\n\n**Sending with Default Notification Titles/Messages/Icons**\n\n```python\n\nfrom notifypy import Notify\n\nnotification = Notify(\n  default_notification_title="Function Message",\n  default_application_name="Great Application",\n  default_notification_icon="path/to/icon.png",\n  default_notification_audio="path/to/sound.wav"\n)\n\ndef your_function():\n  # stuff happening here.\n  notification.message = "Function Result"\n  notification.send()\n```\n\n---\n\n# CLI\nA CLI is available when you install notify-py\n\n```bash\nnotifypy --title --message --applicationName --iconPath --soundPath\n```\nYou may need to add ``python3 -m`` to the beginning.\n\n---\n\n## Important Caveats\n\n- As it stands (May 18, 2020), this is simply a notification service. There is _no_ support for embedding custom actions (buttons, dialogs) regardless of platform. Other then telling you if the shell command was sent, there is also no confirmation on user action on the notification.\n\n- macOS does **not** support custom icons on the fly.. You will need to bundle a customized version of the notifier embedded with your custom icon.\n\n---\n\n### Windows Specific.\n\n- No support for balloon tips (pre Win10).. This will be changed in the future.\n\n---\n\n### Contributors\n\n- [Leterax](https://github.com/Leterax)\n- [jnoortheen](https://github.com/jnoortheen)\n- [dynobo](https://github.com/dynobo)\n- [Xou](https://github.com/GiorgosXou)\n\n\n---\n\n### Inspiration and Special Thanks\n\n- https://github.com/go-toast/toast - Ported their Windows 10 toast notification to Python.\n\n- [Vítor Galvão](https://github.com/vitorgalvao) for https://github.com/vitorgalvao/notificator\n\n- https://notificationsounds.com/notification-sounds/done-for-you-612 example_notification_sound.wav\n\n- https://github.com/mikaelbr/node-notifier\n\n---\n\n# Contributing\n\nContributions are welcome!\n\nPlease base your changes on the latest development branch and open a PR to that branch. PR will not be accepted to the master branch. Tests are ran against all platforms.\n\n### Setting Up Environment\n\n- Install [Poetry](https://python-poetry.org/)\n  - `poetry install`\n- Add patches/new features/bug fiexes\n- Run tests\n  - `poetry run pytest tests/*`\n- Run lints\n  - `poetry run pylint --errors-only notifypy/`\n- Run Black Formatting\n  - `poetry run black notifypy`\n- Open PR to `dev` branch.\n- Add your name to contributors list if you wish!\n',
    'author': 'Mustafa Mohamed',
    'author_email': 'mustafa@ms7m.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ms7m/notify-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
