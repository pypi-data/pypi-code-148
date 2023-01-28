from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.5'
DESCRIPTION = 'zdt'

# Setting up
setup(
    name="zdt",
    version=VERSION,
    author="Dickson",
    author_email="<suwon2912@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['sqlalchemy', 'typing', 'hdbcli','redmail','pandas','datetime','python-dateutil','numpy'],
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






