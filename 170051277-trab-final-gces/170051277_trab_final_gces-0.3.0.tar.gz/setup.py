# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['170051277_trab_final_gces',
 '170051277_trab_final_gces.src',
 '170051277_trab_final_gces.src.data_pipeline',
 '170051277_trab_final_gces.src.data_pipeline.feature_engineering',
 '170051277_trab_final_gces.src.data_pipeline.pre_processing',
 '170051277_trab_final_gces.src.parser',
 '170051277_trab_final_gces.tests',
 '170051277_trab_final_gces.tests.data_pipeline',
 '170051277_trab_final_gces.tests.parser']

package_data = \
{'': ['*'],
 '170051277_trab_final_gces': ['data/*'],
 '170051277_trab_final_gces.src': ['yamls/*'],
 '170051277_trab_final_gces.tests': ['mock/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'MarkupSafe>=2.1.1,<3.0.0',
 'Pillow>=9.4.0,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'altair>=4.2.0,<5.0.0',
 'attrs>=22.2.0,<23.0.0',
 'bpemb>=0.3.4,<0.4.0',
 'certifi>=2022.12.7,<2023.0.0',
 'charset-normalizer>=2.1.0,<3.0.0',
 'contourpy>=1.0.6,<2.0.0',
 'coverage>=7.0.2,<8.0.0',
 'cycler>=0.11.0,<0.12.0',
 'entrypoints>=0.4,<0.5',
 'exceptiongroup>=1.1.0,<2.0.0',
 'fonttools>=4.38.0,<5.0.0',
 'gensim>=3.8.3,<4.0.0',
 'idna>=3.4,<4.0',
 'importlib-resources>=5.10.2,<6.0.0',
 'iniconfig>=1.1.1,<2.0.0',
 'joblib>=1.2.0,<2.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'kiwisolver>=1.4.4,<2.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'packaging>=22.0,<23.0',
 'pandas>=1.5.2,<2.0.0',
 'pkgutil-resolve-name>=1.3.10,<2.0.0',
 'pluggy>=1.0.0,<2.0.0',
 'pyparsing>=3.0.9,<4.0.0',
 'pyrsistent>=0.19.3,<0.20.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.0,<8.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.7,<2023.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'six>=1.16.0,<2.0.0',
 'smart-open>=6.3.0,<7.0.0',
 'threadpoolctl>=3.1.0,<4.0.0',
 'tomli>=2.0.1,<3.0.0',
 'toolz>=0.12.0,<0.13.0',
 'tqdm>=4.64.1,<5.0.0',
 'twine>=4.0.2,<5.0.0',
 'urllib3>=1.26.13,<2.0.0',
 'whatlies>=0.7.0,<0.8.0',
 'zipp>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': '170051277-trab-final-gces',
    'version': '0.3.0',
    'description': 'Pacote utilizado para o deploy do trabalho final da disciplina Gerência de Configuração e Evolução de Software (GCES).',
    'long_description': '# Trabalho individual de GCES 2022-2\n\nOs conhecimentos de Gestão de Configuração de Software são fundamentais no ciclo de vida de um produto de software. As técnicas para a gestão vão desde o controle de versão, automação de build e de configuração de ambiente, testes automatizados, isolamento do ambiente até o deploy do sistema. Todo este ciclo nos dias de hoje são integrados em um pipeline de DevOps com as etapas de Integração Contínua (CI) e Deploy Contínuo (CD) implementadas e automatizada.\n\nPara exercitar estes conhecimentos, neste trabalho, você deverá aplicar os conceitos estudados ao longo da disciplina no produto de software contido neste repositório.\n\nO sistema se trata de uma biblioteca python para executar pipelines de dados de forma customizável em bancos de dados.\n\nPara executar a aplicação em sua máquina, basta seguir o passo-a-passo descritos abaixo.\n\n# Resumo da aplicação \n\n A biblioteca desenvolvida auxilia desenvolvedores a explorar os dados com funções essenciais para a identificação de outliers e anomalias e uma interface que auxilia a visualizar as informações de acordo com o arquivo de configuração.\n\n A biblioteca recebe um arquivo yaml com as configurações de cada etapa do pipeline de dados, e do endereço do banco de dados.\n Após a execução do banco de dados, o banco de dados de dados é atualizado com os resultados da análise e os resultados podem ser visualizados por meio de dashboards no metabase.\n\n# Etapas do Trabalho\n\n## Containerização do Banco\n\n## Containerização da aplicação + metabase\n\n## Gestão de dependencias e pacotes python\n\n##  Integração Contínua (CI)\n',
    'author': 'Nicolas Mantzos',
    'author_email': 'georgeos.nicolas83@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
