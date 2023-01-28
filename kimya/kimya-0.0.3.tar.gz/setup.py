from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'A Simple-to-Use Module About Science.'
LONG_DESCRIPTION = 'A Simple-to-Use Module with Functions About Science (Generally Chemistry). Documentation: ekinpy.github.io/kimya'

# Setting up
setup(
    name="kimya",
    version=VERSION,
    author="https://twitter.com/ekinpy",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['rich', 'requests'],
    keywords=['chemistry', 'python', 'science', 'kimya', 'biology', 'periodic table', 'physics', 'elements'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
	"License :: OSI Approved :: MIT License",
    ]
)