from setuptools import setup

setup(
    name='abbts_blp',
    version='0.0.1',
    author='Pascal Helfenstein',
    author_email='pascal.helfenstien@xemax.ch',
    packages=['abbts_blp'],
    # scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/blp/',
    license='LICENSE.txt',
    description='abbts_blp',
    long_description=open('README.md').read(),
    install_requires=[
        "pyserial >= 3.5",
    ],
)
