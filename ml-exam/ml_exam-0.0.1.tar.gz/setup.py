from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'ml_exam'
LONG_DESCRIPTION = 'for search knowledge uncertainity and optimization '

# Setting up
setup(
    name="ml_exam",
    version=VERSION,
    author="kd_kk",
    author_email="kdkk6161@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['knowledge', 'optimization', 'search', 'uncertainity'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
