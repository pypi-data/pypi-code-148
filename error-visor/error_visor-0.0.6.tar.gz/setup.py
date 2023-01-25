import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.6'
PACKAGE_NAME = 'error_visor'
AUTHOR = 'Victor Valenzuela M'
AUTHOR_EMAIL = 'vi.valenzuelam@gmail.com'
URL = 'https://github.com/vvalenzuela96/error_visor_project'

LICENSE = 'MIT'
DESCRIPTION = 'Librería para guardar registros de errores y warnings personalizados en json'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      #Nothing for now
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)