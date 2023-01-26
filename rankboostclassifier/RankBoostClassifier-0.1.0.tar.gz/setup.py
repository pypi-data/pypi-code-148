## create setup file for creating pypi package

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'RankBoostClassifier'
AUTHOR = 'Suchet Aggarwal, Asmit Kumar Singh, Namrata Bhattacharya, Debarka Sengupta'
AUTHOR_EMAIL = 'suchet18105@iiitd.ac.in, asmit18025@iiitd.ac.in, namrata.bhattacharya@hdr.qut.edu.au, debarka@iiitd.ac.in'
URL = 'https://github.com/cellsemantics/boosted_rank_classifier'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'To add'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

# try:
#     with open('requirements.txt') as f:
#         required = f.read().splitlines()
# except:
#     ## if requirements.txt is not present, throw error
#     required = []
#     raise Exception("Missing requirements")

required = ["imbalanced_learn==0.10.1",
"imblearn==0.0",
"matplotlib==3.6.3",
"numpy==1.23.5",
"pandas==1.5.3",
"scanpy==1.9.1",
"scikit_learn==1.2.1",
"scipy==1.10.0",
"seaborn==0.12.2",
"xgboost==1.7.3"]

INSTALL_REQUIRES = required

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