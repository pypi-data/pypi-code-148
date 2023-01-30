from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.2.0'
DESCRIPTION = 'stalcraft-api unofficial python library'


here = os.path.abspath(os.path.dirname(__file__))


with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="stalcraft-api",
    version=VERSION,
    author="onejeuu",
    author_email="<bloodtrail@beber1k.ru>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    license='MIT',
    keywords=['python', 'stalcraft', 'api'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ]
)
