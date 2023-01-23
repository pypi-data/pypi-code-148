from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'OpenAI Playground for local models'
LONG_DESCRIPTION = 'OpenAI Playground for local models'

# Setting up
setup(
    name="playgroundlocal",
    version=VERSION,
    author="eefh",
    author_email="<ethanhasbrouck02@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['django'],
    keywords=['python', 'ai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)