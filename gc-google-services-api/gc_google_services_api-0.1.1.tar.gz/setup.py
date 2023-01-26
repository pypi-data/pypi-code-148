from setuptools import setup, find_packages
from pathlib import Path

from gc_google_services_api import __version__


this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name='gc_google_services_api',
    version=__version__,
    packages=find_packages(),
    author='Jonathan Rodriguez Alejos',
    author_email='jrodriguez.5716@gmail.com',
    install_requires=open('requirements.txt').read().splitlines(),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
