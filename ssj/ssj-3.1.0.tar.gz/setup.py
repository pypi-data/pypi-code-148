from setuptools import setup
setup(name = 'ssj',
version = '3.1.0',
author = 'Jonathan N. Nagel',
author_email = 'jinnascimento81@gmail.com',
install_requires = ['json', 'os', 'ast', 'cryptography', 'time', 'threading', 'socket'],
packages = ['ssj'],
long_description='Um servidor de NoSQL baseado em JSON e dicionarios Python que facilita o uso em rede local ou em maquina local.',
description = 'Servidor ou gestor de dados em JSON com criptografia Fernet.',
license = 'MIT',
keywords = 'ssj')
