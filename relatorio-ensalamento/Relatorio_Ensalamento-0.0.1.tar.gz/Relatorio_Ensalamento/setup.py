from setuptools import setup, find_packages

setup(name='Relatorio_Ensalamento',
      version='0.1',
      url='https://github.com/capdaccodigos/PUCPR-DAC/blob/master/Relatorio_Ensalamento/Relatorio_Ensalamento_Turmas/Relatorio_Ensalamento.py',
      license='MIT',
      author='mhrrosa',
      author_email='m.rosa1@pucpr.br',
      description='Utilizado para gerar o relatorio ensalamento',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)