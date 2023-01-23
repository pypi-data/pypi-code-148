import sys

from setuptools import find_packages, setup

VERSION = "0.1"
DESCRIPTION = "Markdown extension that make it easier to embed tweets"
LONG_DESCRIPTION = "Markdown extension that make it easier to embed tweets"

# Only install black on Python 3.6 or higher
maybe_black = []
if sys.version_info > (3, 6):
    maybe_black = ["black"]

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="markdowntweetembed",
    version=VERSION,
    author="Colm Britton",
    author_email="<colmjude@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude="tests"),
    install_requires=["markdown", "tweepy"],
    extras_require={
        "test": [
            "flake8",
        ]
        + maybe_black
    },
    keywords=["python", "markdown", "extension", "twitter"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
