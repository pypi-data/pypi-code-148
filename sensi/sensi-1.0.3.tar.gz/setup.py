# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sensi', 'sensi.database', 'sensi.resources']

package_data = \
{'': ['*'],
 'sensi.resources': ['nltk_data/corpora/*',
                     'nltk_data/corpora/stopwords/*',
                     'nltk_data/tokenizers/*',
                     'nltk_data/tokenizers/punkt/*',
                     'nltk_data/tokenizers/punkt/PY3/*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4.45,<2.0.0',
 'Sastrawi>=1.0.1,<2.0.0',
 'aiosqlite>=0.18.0,<0.19.0',
 'nltk>=3.8,<4.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'sensi',
    'version': '1.0.3',
    'description': 'analisis sentimen bahasa Indonesia menggunakan Naive-Bayes',
    'long_description': "<p align=center><i>Library</i> analisis sentiment teks Bahasa Indonesia, menggunakan Klasifikasi Naive-Bayes</p>\n\n## Dependensi\n\n```python\nsastrawi nltk numpy pandas sqlalchemy\n```\n\n## Instalasai\n\n```bash\npip install sensi\n```\n\n## Penggunaan\n\n- [WIKI](https://github.com/GazDuckington/nbc-sentimen/wiki)\n- Contoh penerapan dapat dilihat pada directory 'apis' pada repository [flask-sk](https://github.com/GazDuckington/flask-sk)\n\n- Baca ```resources/predictor.py``` untuk berbagai contoh lainnya.\n\n## Lisensi\n[MIT](./LICENSE)\n",
    'author': 'GazDuckington',
    'author_email': 'dianghazy@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/GazDuckington/nbc-sentimen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
