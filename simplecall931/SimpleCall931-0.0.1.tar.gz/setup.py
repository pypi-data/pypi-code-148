from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='SimpleCall931',
    version='0.0.1',
    license='MIT License',
    author='José Pádua',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='josegabrielpadua@gmail.com',
    keywords='simple calculator',
    description=u'Pacote não oficial',
    packages=['simple'],
    install_requires=['none'],)