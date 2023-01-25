from setuptools import setup, find_packages
from pathlib import Path
this_directory=Path(__file__).parent
long_description=(this_directory/"README.md").read_text()

setup(
    name='MolLayers',
    version='0.1.2',
    packages=find_packages(where='src'),
    package_dir={'':'src',
                 },
    include_package_data=True,
    install_requires=['biopython>=1.7',
                      'mmtf-python>=1.1',
                      ],
    url='https://www.nbrkarampudi.org',
    license='GNU GPL3',
    author='nbrkarampudi',
    author_email='nagabhushan.k@srmap.edu.in',
    description='Implementation of Layers algorithm adapting Biopython file parsers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers = ['Environment :: Console',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   ],

)
