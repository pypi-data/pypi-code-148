from codecs import open
from os import path

from setuptools import setup

# Package Version
VERSION = '1.0.2'

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pascal-voc-toolkit',
    version=VERSION,
    packages=['tests', 'pascal_voc_toolkit'],
    url='',
    license='',
    author='Aman Khatri',
    author_email='amankhatri.ai@gmail.com',
    description='Set of tools to work with Pascal VOC annotation format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=['dict2xml==1.7.2', 'xmltodict==0.13.0', 'pytest==7.2.1', 'opencv-python==4.7.0.68']
)
