from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.2'
DESCRIPTION = 'Script implementing TOPSIS'


# Setting up
setup(
    name="102003634",
    version=VERSION,
    author="Falguni Sharma",
    author_email="falguni7572@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    entry_points={
        'console_scripts': [
            'topsis=topsisLibrary.topsis:main'
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.5',
)