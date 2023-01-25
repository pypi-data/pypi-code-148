from setuptools import setup, find_packages

VERSION = "0.0.1"


setup(
    name = 'plinko',
    version = VERSION,
    author = 'Nat Hawkins, Mike Chappelow',
    author_email = 'nat.hawkins@kellogg.com, michael.chappelow@kellogg.com',
    description = 'Python equivalent to the internal R library, klink, for establishing remote connections to data sources',
    long_description = open('README.md').read(),
    license = 'LICENSE.txt',
    packages = find_packages(),
    scripts = [],
    install_requires=[],
    url = ''
)