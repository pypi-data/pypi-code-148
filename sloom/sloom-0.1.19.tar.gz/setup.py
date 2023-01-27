
import pathlib
from setuptools import setup, find_packages
from version import Version

v = Version()

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.' + str(v.version)
PACKAGE_NAME = 'sloom'
AUTHOR = 'Reed Hunsaker'
AUTHOR_EMAIL = 'reed.hunsaker@gmail.com'
URL = 'https://github.com/ReedHunsaker/Webscraper'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Webscraper'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'requests',
      'bs4',
      'pytest'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )