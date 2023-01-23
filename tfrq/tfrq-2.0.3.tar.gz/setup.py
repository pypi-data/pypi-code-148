from setuptools import setup


def readme():
    with open('README.rst', "r", encoding="utf8") as f:
        return f.read()


setup(
    name='tfrq',
    version='2.0.3',
    description='A library to parallelize the execution of a function in python',
    author='Foad Abo Dahood',
    long_description=readme(),
    author_email='Foad.ad5491@gmail.com',
    py_modules=['tfrq'],
    install_requires=['futures==2.2.0'],
)
