from setuptools import setup, find_packages
from distutils.core import setup

VERSION = '0.0.1'
DESCRIPTION = "Your most beloved fancy logger. It's colorful and shiny"


# Setting up
setup(
    name="brand-new-fancy-logger",
    version=VERSION,
    author="Kaja",
    author_email="<karolina.rzepiela95@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'logging'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)