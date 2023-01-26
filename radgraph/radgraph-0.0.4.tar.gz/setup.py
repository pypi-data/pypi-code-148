import pathlib
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    sys.exit('Sorry, Python >=3.8 is required for radgraph.')

setup(
    name='radgraph',
    version='0.0.4',
    author='Jean-Benoit Delbrouck',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.8',
    install_requires=['torch>=1.8.1',
                      'transformers==4.23.1',
                      "appdirs",
                      'overrides==3.1.0',
                      'jsonpickle',
                      'filelock',
                      'h5py',
                      'spacy',
                      'nltk',
                      ],
    py_modules=['radgraph'],
    zip_safe=False)
