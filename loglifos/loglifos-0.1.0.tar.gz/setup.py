# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loglifos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'loglifos',
    'version': '0.1.0',
    'description': 'A log helper',
    'long_description': '# A logger python project\n```\n ,-----------------------------------------------------------------v\n u           ,-~~\\   <~)_   u\\             /\\    ,-.       ,-.     u\n u  _,===-.,  (   \\   ( v~\\ u u  _,===-.,  \\/   <,- \\_____/  `     u\n u (______,.   u\\. \\   \\_/\'  \\u (______,. /__\\    /  ___. \\  -===- u\n u            _a_a`\\\\  /\\     u           \\--/ ,_(__/ ,_(__\\       u\n `--------------------------------------------- By CenturyBoys ----y\n```\n\nThis is a non block JSON logger that use python\'s default logger with a thread executor.\n\nBy default loglifos set the default root loger to ERROR level\n\n### Settings\n\nYou can change loglifos log level using ```set_config``` method. Loglifos use the same level constants as the default logging python lib. \n\n ```python\nimport loglifos\n\nloglifos.set_config(loglifos.ERROR)\n```\n\n### Using\n\n```python\nimport loglifos\n\ntry:\n    a = 1 / 0 \nexcept Exception as e:\n    loglifos.debug("Message from debug", "some args", 1, some__kwargs="Kwargs of debug")\n    loglifos.info("Message from info", "some args", 1, some__kwargs="Kwargs of info")\n    loglifos.warning("Message from warning", "some args", 1, some__kwargs="Kwargs of warning")\n    loglifos.error("Message from error", "some args", 1, some__kwargs="Kwargs of error", exception=e)\n    loglifos.critical("Message from critical", "some args", 1, some__kwargs="Kwargs of critical")\n```\n```bash\n{"time": "2023-01-25 13:27:34.896765", "level": "ERROR", "file": "/home/marco/.config/JetBrains/PyCharmCE2022.3/scratche\n  s/scratch_1.py", "function": "<module>", "msg": "Message from error", "some__kwargs": "\'Kwargs of error\'", "args": "(\'\n  some args\', 1)", "error": "Traceback (most recent call last):\\n  File \\"/home/marco/.config/JetBrains/PyCharmCE2022.3/\n  scratches/scratch_1.py\\", line 9, in <module>\\n    a = 1 / 0\\nZeroDivisionError: division by zero\\n"}\n{"time": "2023-01-25 13:27:34.899420", "level": "DEBUG", "file": "/home/marco/.config/JetBrains/PyCharmCE2022.3/scratche\n  s/scratch_1.py", "function": "<module>", "msg": "Message from debug", "some__kwargs": "\'Kwargs of debug\'", "args": "(\'\n  some args\', 1)"}\n{"time": "2023-01-25 13:27:34.899676", "level": "INFO", "file": "/home/marco/.config/JetBrains/PyCharmCE2022.3/scratches\n  /scratch_1.py", "function": "<module>", "msg": "Message from info", "some__kwargs": "\'Kwargs of info\'", "args": "(\'som\n  e args\', 1)"}\n{"time": "2023-01-25 13:27:34.899885", "level": "WARNING", "file": "/home/marco/.config/JetBrains/PyCharmCE2022.3/scratc\n  hes/scratch_1.py", "function": "<module>", "msg": "Message from warning", "some__kwargs": "\'Kwargs of warning\'", "args\n  ": "(\'some args\', 1)"}\n{"time": "2023-01-25 13:27:34.900066", "level": "CRITICAL", "file": "/home/marco/.config/JetBrains/PyCharmCE2022.3/scrat\n  ches/scratch_1.py", "function": "<module>", "msg": "Message from critical", "some__kwargs": "\'Kwargs of critical\'", "a\n  rgs": "(\'some args\', 1)"}\n```\n',
    'author': 'Marco Sievers de Almeida Ximit Gaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
