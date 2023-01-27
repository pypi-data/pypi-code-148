# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['honorific']

package_data = \
{'': ['*']}

install_requires = \
['pymorphy2>=0.9.1,<0.10.0', 'spacy>=3.4.3,<4.0.0', 'twine>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'honorific',
    'version': '0.1.5',
    'description': 'Изменение числа во втором лице',
    'long_description': '# honorific\n\nДанный пакет позволяет изменять форму обращения к человеку.\nС неформальной ("ты") на более уважительную ("Вы"), и наоборот.\n\n## Установка\nУстановка пакета\n```bash\npython -m pip install honorific\n```\nПри первом запуске скачается пакет *ru_core_news_lg* для *spacy*, но можно установить его заранее\n\n```bash\npython -m spacy download ru_core_news_lg\n```\n\n## Пример\n\n```python\n>>> honorific.honor("Как твои дела?")\n\'Как ваши дела?\'\n\n>>> honorific.honor("Так ты скажешь, откуда ты?")\n\'Так вы скажете, откуда вы?\'\n```\n\n## Описание\n\nВ данный момент обрабатываются \n* глаголы\n* местоимения\n* краткие прилагательные и причастия(+модальные глаголы).\n\n## TODO\n* обработка глаголов в прошедшем времени в СПП  \n* обработка сложных конструкций(пропуск пунктуации и т.д)  \n* обработка устойчивых выражений("ух ты" и т.д.)  \n* обработка возвратно-притяжательных местоимений\n\n# Метрики\n* Gold Standart - соответствие проф. разметке = 100%\n* Adequacy - соответствие нормам русского языка = 94%\n* Accuracy - правильность измененных словоформ = 100%\n\n\n',
    'author': 'Viktor Merkurev',
    'author_email': 'v.merkurev@promo-bot.ru',
    'maintainer': 'VMerkurev',
    'maintainer_email': 'v.merkurev@promo-bot.ru',
    'url': 'https://git.promo-bot.ru/v.merkurev/honorific',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
