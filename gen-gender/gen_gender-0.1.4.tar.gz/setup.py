# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gen_gender']

package_data = \
{'': ['*'], 'gen_gender': ['pkl/*', 'txt/*']}

install_requires = \
['stanza>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'gen-gender',
    'version': '0.1.4',
    'description': 'Изменение рода ответа с мужского на женский',
    'long_description': '# gen_gender\n\nПакет позволяет сменить род ответов с мужского на женский.\n\n## Пример\n\n```python\n>>> gen_gender.swap("Я тот самый учитель.")\n"Я та самая учительница"\n\n>>> gen_gender.swap("Я не женат. У меня два брата и одна сестра.")\n"Я не замужем, у меня два брата и одна сестра."\n```\n\n## Типы обрабатываемых замен\n\n- Замена рода выполняется только для конструкций в 1 лице ед. числе\n- Замена сказумых, выраженных глаголом в прошедшем времени\n- Замена дополнений, выраженных соуществительным с зависимым прилагательным\n- Замена зависимых от существительного в 1 лице ед. числе или местоимения причастных и деепричестных оборотов\n- Замена указательных, притяжательных, неопределенных, относительных, определительных, отрицательных местоимений\n\n## Используемые библиотеки\n\n- pymorphy3\n- stanza\n\n## Дополнительные файлы\n\n- src/pkl словари альтернатив\n- src/txt оригинальные файлы для редактирования\n\n',
    'author': 'vmerkurev',
    'author_email': 'v.merkurev@promo-bot.ru',
    'maintainer': 'VMerkurev',
    'maintainer_email': 'v.merkurev@promo-bot.ru',
    'url': 'https://git.promo-bot.ru/v.merkurev/gen_gender',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
