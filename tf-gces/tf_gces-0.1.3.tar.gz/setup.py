# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.data_pipeline',
 'src.data_pipeline.feature_engineering',
 'src.data_pipeline.pre_processing',
 'src.parser',
 'tests',
 'tests.data_pipeline',
 'tests.parser']

package_data = \
{'': ['*'],
 'src': ['yamls/*'],
 'tests': ['mock/*', 'mock/fail/*', 'mock/success/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'MarkupSafe>=2.1.1,<3.0.0',
 'Pillow>=9.4.0,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'altair>=4.2.0,<5.0.0',
 'attrs>=22.2.0,<23.0.0',
 'bpemb>=0.3.4,<0.4.0',
 'certifi>=2022.12.7,<2023.0.0',
 'charset-normalizer>=2.1.1,<3.0.0',
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
 'pylint>=2.15.10,<3.0.0',
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
 'urllib3>=1.26.13,<2.0.0',
 'whatlies>=0.7.0,<0.8.0',
 'zipp>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'tf-gces',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Trabalho individual de GCES 2022-2\n\n\nOs conhecimentos de Gestão de Configuração de Software são fundamentais no ciclo de vida de um produto de software. As técnicas para a gestão vão desde o controle de versão, automação de build e de configuração de ambiente, testes automatizados, isolamento do ambiente até o deploy do sistema. Todo este ciclo nos dias de hoje são integrados em um pipeline de DevOps com as etapas de Integração Contínua (CI) e Deploy Contínuo (CD) implementadas e automatizada.\n\nPara exercitar estes conhecimentos, neste trabalho, você deverá aplicar os conceitos estudados ao longo da disciplina no produto de software contido neste repositório.\n\nO sistema se trata de uma biblioteca python para executar pipelines de dados de forma customizável em bancos de dados.\n\nPara executar a aplicação em sua máquina, basta seguir o passo-a-passo descritos abaixo.\n\n# Resumo da aplicação \n\n A biblioteca desenvolvida auxilia desenvolvedores a explorar os dados com funções essenciais para a identificação de outliers e anomalias e uma interface que auxilia a visualizar as informações de acordo com o arquivo de configuração.\n\n A biblioteca recebe um arquivo yaml com as configurações de cada etapa do pipeline de dados, e do endereço do banco de dados.\n Após a execução do banco de dados, o banco de dados de dados é atualizado com os resultados da análise e os resultados podem ser visualizados por meio de dashboards no metabase.\n\n # Etapas do Trabalho\n\n O trabalho deve ser elaborado através de etapas. Cada uma das etapas deve ser realizada em um commit separado com o resultado funcional desta etapa.\n\nAs etapas de 1 a 3 são relacionadas ao isolamento do ambiente utilizando a ferramenta Docker e Docker Compose. Neste sentido o tutorial abaixo cobre os conceitos fundamentais para o uso destas tecnologias.\n\n[Tutorial de Docker](https://github.com/FGA-GCES/Workshop-Docker-Entrega-01/tree/main/tutorial_docker)\n\nAs etapas de 4 e 5 são relacionadas à configuração do pipeline de CI e CD.\n\n[Tutorial CI - Gitlab](https://github.com/FGA-GCES/Workshop-CI-Entrega-02/tree/main/gitlab-ci_tutorial)\n\n\n## Containerização do Banco\n\n\nA versão inicial do sistema contém o metabase no backend cujo funcionamento requer uma instalação de um banco de dados Mongo. A primeira etapa do trabalho é de configurar um container somente para o banco de dados com as credenciais especificadas na descrição da aplicação e testar o funcionamento do mesmo.\n\n### RESOLUÇÃO\n\nFoi criado um arquivo docker-compose.yml que continha apenas um container do mongodb a partir da imagem "mongo"\n\n\n## Containerização da aplicação + metabase\n\nNesta etapa, tanto o a aplicação python quanto o metabase/banco deverão estar funcionando em containers individuais.\n\nDeverá ser utilizado um orquestrador (Docker Compose) para gerenciar comunicação entre os containers além do uso de credenciais, networks, volumes, entre outras configurações necessárias para a correta execução da aplicação.\n\n### RESOLUÇÃO\n\nFoi criado um Dockerfile para o app (lib python).\nNo arquivo docker-compose.yml foram adicionados dois containeres novos, o do metabase e o do app (que builda a partir da Dockerfile). Foi também criada uma network (tipo bridge) para comunicação entre os conteineres do metabase e do mongodb.\n\n## Gestão de dependencias e pacotes python\n\nConfigurar o gerenciador de dependencias e pacotes python, o poetry, para gerar um pacote pip da solução. Publicar a biblioteca\n\nhttps://python-poetry.org\n\n### RESOLUÇÃO\n\nFoi rodado \'\'\'poetry init\'\'\' e criado um arquivo pyproject.toml e foram adicionadas configurações da lib e todas suas dependencias, após isso foi rodado o comando \'\'\'poetry publish --build\'\'\', para publicar a lib manualmente no PyPI.\nLink da lib: https://pypi.org/project/tf-gces/\n\n## Documentação automatizada\n\nGerar a documentação da biblioteca de forma automatizada utilizando o doxygen para gerar informacoes da biblioteca e o sphinx para criar documentação https://www.sphinx-doc.org\n\n### RESOLUÇÃO\nPrimeiro instalei o doxygen localmente e criei uma doxyfile, nessa doxyfile coloquei o README.md e o diretório src de forma recursiva para documentar todos os arquivos. Também configurei para gerar apenas XML. Após isso consegui gerar os XML com o comando \'\'\'doxygen Doxyfile\'\'\'. Instalei o breathe e o sphinx, criei o arquivo de configuração do sphinx conf.py e configurei o breathe la dentro e o adicionei como extensão. Após isso rodei \'\'\'sphinx-build -b html . ./docs\'\'\' para gerar uma documentação em HTML na pasta ./docs.\n\n\n##  Integração Contínua (CI)\n\nPara a realização desta etapa, a aplicação já deverá ter seu ambiente completamente containerizado.\n\nDeverá ser utilizada uma ferramenta de Integração Contínua para garantir o build, os testes e o deploy para o https://pypi.org .\n\nEsta etapa do trabalho poderá ser realizada utilizado os ambientes de CI do GitLab-CI ou Github Actions.\n\nRequisitos da configuração da Integração Contínua (Gitlab ou Github) incluem:\n\nBuild (Poetry)\nTest - unitários\nLint - Pylint\nDocumentação (sphinx)\n\n### RESOLUÇÃO\nPrimeiramente foi criado o workflow que é rodoado em qualquer push na main.\nComecei instalando o python e o poetry, atravez do actions/setup-python@v4 e do abatilo/actions-poetry@v2 (achei no marketplace).\nApós isso rodo um \'\'\'poetry install\'\'\', que installa todas a dependências.\n\nDepois rodei os testes \'\'\'poetry run pytest tests\'\'\', como não há nenhum teste na pasta tests, ele falhava e não rodava o resto do job, para isso criei um placeholder de teste na pasta tests, que simplesmente passa. Com isso a etapa de rodar os testes tem sucesso.\n\nApós isso o job faz uma checagem de lint, utilizei o pylint (que foi adicionado nas dependencias do poetry e ja instalado), e rodo \'\'\'poetry run pylint --fail-under=7 src\'\'\', para passar, tem que ter uma qualidade de código acima 7/10. Para atingir essa qualidade, com ajuda da extensão black, formatei todos os arquivos do projeto e commitei. (A qualidade inicial era 2/10). Com isso a etapa de lint passa.\n\nPara gerar a documentação, instalei o oxygen manualmente no ubuntu que está rodando o workflow, e gerei o XML a partir do Doxyfile que foi criado na parte de documentação. Instalei o breathe e o Sphinx através do Pip e gerei a documentação final com o Sphinx em HTML na pasta docs, adicionei essa pasta também no pyproject.toml para ela ser publicada junto com a biblioteca no PyPI.\n\nDepois de instalar dependencias, rodar testes, lint e gerar a documentação atualizada, realizo o build com o poetry. \n\nApós o build é finalmente possível publicar a nova release no PyPI, eu gero uma nova versão (ex: de 0.0.1 vai para 0.0.2) e publico do PyPI. Link da biblioteca: https://pypi.org/project/tf-gces/ .\n\nA lib contém também a pasta docs, com a documentação atualizada gerada pelo sphinx.\n\n\n## Avaliação\n\nA avaliação do trabalho será feita à partir da correta implementação de cada etapa. A avaliação será feita de maneira **quantitativa** (se foi realizado a implementação + documentação), e **qualitativa** (como foi implementado, entendimento dos conceitos na prática, complexidade da solução). Para isso, faça os **commits atômicos, bem documentados, completos** a fim de facilitar o entendimento e avaliação do seu trabalho. Lembrando o trabalho é individual.\n\n**Observações**: \n1. A data final de entrega do trabalho é o dia 28/01/2023;\n2. O trabalho deve ser desenvolvido em um **repositório PESSOAL e PRIVADO** que deverá ser tornado público somente após a data de entrega do trabalho (no dia 28/01/2023);\n3. Cada etapa do trabalho deverá ser entregue em commits progressivos (pendendo ser mais de um commit por etapa);\n4. Os **commits devem estar espaçados em dias ao longo do desenvolvimento do trabalho**. Commits feitos todos juntos na data de entrega não serão descontados da nota final.\n\n| Item | Peso |\n|---|---|\n| 1. Containerização do Banco                      | 1.0 |\n| 2. Containerização da biblioteca + Banco          | 1.5 |\n| 3. Publicação da biblioteca  | 1.5 |\n| 4. Documentação automatiza | 1.5 |\n| 5. Integração Contínua (Build, Test, Lint, documentacao)       | 3.0 |\n| 6. Deploy Contínuo                               | 1.5 |\n\n\n##  Exemplo de Trabalhos Anteriores\n\nAlguns trabalhos de trabalhos anteriores:\n\n- [2020/2](https://github.com/FGA-GCES/Trabalho-Individual-2020-2)\n- [2021/1](https://github.com/FGA-GCES/Workshop-Docker-Entrega-01)\n- [2021/2](https://github.com/FGA-GCES/Trabalho-Individual-2021-2)\n\n\n\n### Requisitos de instação\n\n```\npython -m venv env\nsource env/bin/activate\npip install -r requirements.txt\n```\n\n### Rodando a aplicação\n\n```\npython src/main.py\n```\n\n### Testando\n\n```\npytest --cov\n```\n\n### Metabase\n\nO metabase ajuda a visualizar e a modelar o processamento dos dados, a engenharia de features e monitoramento do modelo.\n\n\n\n| Keywords  | Descrição |\n|-----------|-------------|\n|   CSV     | Um arquivo CSV é um arquivo de texto simples que armazena informações de tabelas e planilhas. Os arquivos CSV podem ser facilmente importados e exportados usando programas que armazenam dados em tabelas.|\n| Collection (coleção)| Uma coleção é um agrupamento de documentos do MongoDB. Os documentos dentro de uma coleção podem ter campos diferentes. Uma coleção é o equivalente a uma tabela em um sistema de banco de dados relacional.|\n|  Database | Um banco de dados armazena uma ou mais coleções de documentos.|\n| Mongo| É um banco de dados NoSQL desenvolvido pela MongoDB Inc. O banco de dados MongoDB foi criado para armazenar uma grande quantidade de dados e também executar rapidamente.|\n\n\n\n**Connect the database to the metabase**\n\n- step 1: Open localhost:3000\n- step 2: Click Admin setting\n- step 3: Click Database\n- step 4: Adicione os dados de autenticação de  banco de dados \n\n\n**Exemplo da conexão mongo  metabase**\n|  metabase  | credential  |\n|------------|-------------|\n|    host    |  mongo  |\n|dabase_name | use the name you define in make migrate|\n|    user    |   lappis    |\n|  password  |   lappis    |\n\n',
    'author': 'Christian Fleury',
    'author_email': 'chfleurysiq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
