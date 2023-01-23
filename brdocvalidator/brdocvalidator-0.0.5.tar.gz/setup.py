from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Library to validate brazilians documents, email, birthDate and others'
LONG_DESCRIPTION = 'Library to validate brazilians documents, email, birthDate and others'

# Setting up
setup(
    name="brdocvalidator",
    version=VERSION,
    author="rafaelscone (Rafael Schneider)",
    author_email="<pipbrvalidator@impaire.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['bcrypt'],
    keywords=['python', 'validation', 'cpf', 'cnpj'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
