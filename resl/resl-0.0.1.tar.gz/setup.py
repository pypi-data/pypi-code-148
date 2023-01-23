from setuptools import setup

__version__ = '0.0.1'

setup(
    name = 'resl',
    version = __version__,
    author = 'Callope',
    description = 'Minimal reverse shell.',
    packages = ['resl'],
    python_requires='>=3.5',
    install_requires = [
        'setuptools',
    ],
    entry_points = {
        'console_scripts': ['resl=resl.cli:main'],
    }
)
