# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsapy']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'colorama>=0.4.5,<0.5.0',
 'gmpy2>=2.1.2,<3.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'nltk>=3.7,<4.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'regex>=2022.4.24,<2023.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.8.1,<2.0.0',
 'setuptools>=62.3.2,<63.0.0',
 'six>=1.16.0,<2.0.0',
 'unicodedata2>=14.0.0,<15.0.0',
 'wheel>=0.37.1,<0.38.0',
 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'vsapy',
    'version': '0.8.0',
    'description': 'Vector Symbolic Architecture(VSA) library that allows building VSA apps that use various flavours of VSA vectors.',
    'long_description': '# vsapy - Vector Symbolic Architecture(VSA) library.\nThis library implements the common methods used in hyperdimensional computing/Vector Symbolic Architectures. Namely\n`bind`, `unbind` and some bundling operations, `bag`, `ShiftedBag`, `NamedBag` and a hierarchical bundling \nmethod `CSPvec`. The main objective of the library is to enable a single API to cater for various flavours of VSA, \nincluding `Binary Spatter Codes`, `Ternary`, `TernaryZero`, `Laiho` and `LaihoX` (a simplified `Laiho` that \nis faster and supports incremental bundling without catastrophic forgetting). \n\nA set of demo test cases are supplied to demonstrate the use of the library calls.\n\n\n## If installing from PyPi simply\n  - Poetry add vsapy\n<br/>or<br/>\n  - pip install vsapy (into your environment)\n\n## Installing from source\n  - clone the code to a directory of your choice, say "vsapy"\n\n### Installing Dependancies  \n- Poetry: the easiest way is using poetry\n  - cd vsapy\n  - poetry install\n  - poetry shell  (to activate the environment)\n  \n\n- pip install vsapy\n  - create an environment using your favorite environment manager\n  - e.g. conda create -n vsapy39 python=3.9\n  - conda activate vsapy39\n  - pip install -r requirements.txt\n\n### Usage\nHint: Valid values for `VSaType` are, `VsaType.BSC`, `VsaType.Laiho`, `VsaType.LaihoX`(fastest), `VsaType.Tern`, \n`VsaType.TernZero` and `VsaType.HRR`\\\n(** Note, the demos listed below will not run with type `VsaType.HRR` **). <br/><br/>\n\n\n- For examples of using the vsapy library, see the code examples in the ./tests directory. Note there are no \ncommand-line arguments implemented for the tests at the moment. To change the type of VSA in use, edit the code changing\n`vsa_type=VsaType.BSC` as mentioned below. All of the test cases can be run by simply invoking from the command line, \ne.g., `$python cspvec_sequence.py`.\n\n\n\n  - `cspvec_sequence.py`: This is the most straightforward demo. Try this first. It demonstrates building a sentence as \na vsa sequence and stepping forward & backwards. Change `vsa_type=VsaType.BSC` in the code to change the type of VSA\nused to build the representation. <br/><br/>\n  \n  - `build_docs.py`: demonstrates combining large documents into a hierarchical vsa code book. The top-level document \nvector is a high-level semantic representation of the entire document. Change `vsa_type=VsaType.BSC` in the code to \nchange the type of VSA used to build the representation. <br/><br/>\n\n    - `load_docs.py`: compares the document vectors built using `build_docs.py` at various levels in the \ndocument hierarchy. <br/><br/> Change `levels_to_extract = [0, 1]`, `0=top-level document vectors`, `1=Act-level vectors`, \n`2=Scene-level vectors` and so on (Can set to any level, e.g., `levels_to_extract = [2]` would compare only \nScene-level vectors). <br/><br/>\n\n      - Understanding output names: `OE_=Old English`, `NE_=New English`, `nf_=NoFear Shakespeare`, `tk_=NLTK Shakespeare`,\n`og_=Alternate Shakespeare`, `ham=Shakespeare\'s Hamlet` , `mbeth=Shakespeare\'s Macbeth`. <br/><br/> \n\n  - `json2vsa.py`: demonstrates the creation of a VSA vector from an input JSON file and shows a comparison of various\nJSONs using VSA. Change `vsa_type=VsaType.BSC` in the code to change the type of VSA used to build the representation.\n\n\n',
    'author': 'Chris Simpkin',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vsapy/vsapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
