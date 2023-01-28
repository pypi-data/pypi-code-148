# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynalytics',
 'pynalytics.data_pipeline',
 'pynalytics.data_pipeline.feature_engineering',
 'pynalytics.data_pipeline.pre_processing',
 'pynalytics.parser']

package_data = \
{'': ['*'], 'pynalytics': ['yamls/*']}

install_requires = \
['Jinja2==3.1.2',
 'MarkupSafe==2.1.1',
 'Pillow==9.4.0',
 'PyYAML==6.0',
 'altair==4.2.0',
 'attrs==22.2.0',
 'bpemb==0.3.4',
 'certifi==2022.12.7',
 'charset-normalizer==2.1.1',
 'contourpy==1.0.6',
 'coverage==7.0.2',
 'cycler==0.11.0',
 'entrypoints==0.4',
 'exceptiongroup==1.1.0',
 'fonttools==4.38.0',
 'gensim==3.8.3',
 'idna==3.4',
 'importlib-resources==5.10.2',
 'iniconfig==1.1.1',
 'joblib==1.2.0',
 'jsonschema==4.17.3',
 'kiwisolver==1.4.4',
 'matplotlib==3.6.2',
 'numpy==1.24.1',
 'packaging==22.0',
 'pandas==1.5.2',
 'pkgutil-resolve-name==1.3.10',
 'pluggy==1.0.0',
 'pyparsing==3.0.9',
 'pyrsistent==0.19.3',
 'pytest-cov==4.0.0',
 'pytest==7.2.0',
 'python-dateutil==2.8.2',
 'pytz==2022.7',
 'requests==2.28.1',
 'scikit-learn==1.2.0',
 'scipy==1.9.3',
 'sentencepiece==0.1.97',
 'six==1.16.0',
 'smart-open==6.3.0',
 'threadpoolctl==3.1.0',
 'tomli==2.0.1',
 'toolz==0.12.0',
 'tqdm==4.64.1',
 'urllib3==1.26.13',
 'whatlies==0.7.0',
 'zipp==3.11.0']

entry_points = \
{'console_scripts': ['main = pynalytics.main:']}

setup_kwargs = {
    'name': 'pynalytics',
    'version': '0.2.0',
    'description': 'This is a lib from developed for the individual work related to the Software Evolution and Configuration Management subject from UnB - Universidade de Brasília during the 2022.2 semester',
    'long_description': '# Trabalho individual de GCES 2022-2\n\n# Pynalytics\n\n A biblioteca desenvolvida auxilia desenvolvedores a explorar os dados com funções essenciais para a identificação de outliers e anomalias e uma interface que auxilia a visualizar as informações de acordo com o arquivo de configuração.\n\n A biblioteca recebe um arquivo yaml com as configurações de cada etapa do pipeline de dados, e do endereço do banco de dados.\n Após a execução do banco de dados, o banco de dados de dados é atualizado com os resultados da análise e os resultados podem ser visualizados por meio de dashboards no metabase.\n\n# Requisitos\n\n- Python 3.9.16\n- Poetry 1.3.2\n- Docker\n\n\n\n\n',
    'author': 'João Pedro Chaves',
    'author_email': 'joaopedroaschaves@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JPedroCh/Trabalho-Individual-2022-2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.9.16',
}


setup(**setup_kwargs)
