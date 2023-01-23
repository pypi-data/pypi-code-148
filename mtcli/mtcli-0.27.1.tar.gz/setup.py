# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtcli', 'mtcli.pa']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'metatrader5>=5.0.43,<6.0.0',
 'numpy>=1.24,<2.0',
 'python-dotenv>=0.19,<0.20']

entry_points = \
{'console_scripts': ['mt = mtcli.mt:mt']}

setup_kwargs = {
    'name': 'mtcli',
    'version': '0.27.1',
    'description': 'Converte gráfico do MetaTrader 5 para texto',
    'long_description': '# mtcli  \n  \nAplicativo de Linha de comando para converter dados do MetaTrader 5 para formato TXT.  \nO formato TXT é especialmente acessado por tecnologias assistivas para cegos.  \n\n[mtcli no PyPI](https://pypi.python.org/pypi/mtcli)  \n  \n## Pré-requisitos  \n\n* [MetaTrader 5](https://www.metatrader5.com/pt) - Plataforma de trading.  \n* [Indicador mtcli](https://tinyurl.com/vfranca-mtcli) - programa MQL5 executado no MetaTrader 5.  \n* [Python](https://www.python.org/downloads/windows) - Interpretador de comandos.  \n\n\n## Instalação  \n\n1. Instalar o MetaTrader 5.  \n2. Executar o indicador mtcli.ex5 e anexar a um gráfico.  \n3. Instalar o Python:\n\n```cmd\nwinget install python\n```\n\n4. Instalar o mtcli:\n\n```cmd\npip install mtcli\n```\n\n\n\nOpcionalmente baixe a pasta mtcli e descompacte os arquivos em C:\\mtcli.  \n[clique aqui para fazer o download](https://tinyurl.com/vfranca-mtcli-pasta)\n\n## Comandos  \n  \n```cmd\nmt bars <codigo_do_ativo> \n```\nExibe as últimas 40 barras diárias  do ativo.  \nDigite mt bars --help para ver as opções.  \n\n```cmd\nmt mm <codigo_do_ativo>\n```\nExibe a média móvel simples das últimas 20 barras diárias do ativo.  \nDigite mt mm --help para ver as opções.  \n\n\n```cmd\nmt rm <codigo_do_ativo>\n```\nExibe o range médio das últimas 14 barras diárias do ativo.  \nDigite mt rm --help para ver as opções.  \n\n```cmd\nmt ma <codigo_do_ativo>\n```\nExibe as médias móveis das 20 barras diárias do código conforme exportadas pelo indicador MA_TXT.  \nDigite mt ma --help para ver as opções.  \n[Clique aqui para baixar o indicador MA_TXT](https://tinyurl.com/vfranca-ma-txt)  \nObservação: é necessário anexar o indicador MA_TXT ao gráfico e configurar para exportar as 20 barras do diário.  \n\n\n## Agradecimentos  \n  \nAo @MaiconBaggio fornecedor do primeiro EA exportador das cotações para CSV.  \nAo Claudio Garini que transferiu a exportação das cotações para um indicador.  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vfranca/mtcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
