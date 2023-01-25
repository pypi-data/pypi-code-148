from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

with open('README.md','r') as arq:
    readme = arq.read()

setup(name='Relatorio_Ensalamento',
    version='0.0.1',
    license='MIT License',
    author='Matheus Henrique Rosa',
    long_description=readme,
    long_description_content_type="",
    author_email='m.rosa1@pucpr.br',
    keywords='Relatorio Ensalamento',
    description=u'Utilizado para gerar o relatorio ensalamento',
    packages=['Relatorio_Ensalamento'],
    install_requires=['requests'],)