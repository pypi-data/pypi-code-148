# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))  # enables relative local imports

import setup

"""

https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://choosealicense.com/licenses/mit/
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cbl_test_package==1.2.3

### packages: build, twine

python3 -m build 
python3 -m twine upload dist/cbl-0.2.1*


python3 -m build  
python3 -m twine upload --repository testpypi dist/* 
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cbl_test_package@1.2.3 


python3 -m twine upload dist/* 
python3 -m pip install cbl_test_package==1.2.3 
pip install cbl-test-package==1.2.3
pip install cbl-test-package==2.3.4
"""

