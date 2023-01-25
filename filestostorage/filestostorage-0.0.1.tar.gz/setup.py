from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'store files in database'
LONG_DESCRIPTION = 'A package which is used to store files such as .jpeg,.jpg,.mp4,.mp3,.pdf,.dox with minimum loc '
# Setting up
setup(
    name="filestostorage",
    version=VERSION,
    author="ngit_kmit",
    author_email="devikarubir@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['ngitkmit','store files', 'database', 'store', 'file', 'ngit','mongo','kmit'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)