from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '2.3.7.1'
DESCRIPTION = 'A package to scrape Amazon product description using Selenium.'

# Setting up
setup(
    name="amasel",
    version=VERSION,
    author="Shamim Mahbub",
    author_email="sha237mim@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= "",
    packages=find_packages(),
    install_requires=['selenium'],
    keywords=['python', 'amazon_scrape', 'selenium'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)