from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='base_ouro',
    version='9.1',
    author='Gabriel Ernesto Barboza Pereira',
    author_email='ernesto.gabriel@pucpr.br',
    packages=['base_ouro'],
    description='Conversor utilizado para a geração da Base Ouro',
    long_description=readme,
    license='MIT',
    keywords='conversor base_ouro',
)
