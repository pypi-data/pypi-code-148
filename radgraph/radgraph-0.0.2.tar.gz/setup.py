import pathlib
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    sys.exit('Sorry, Python >=3.8 is required for ViLMedic.')

setup(
    name='radgraph',
    version='0.0.2',
    author='Jean-Benoit Delbrouck',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.8',
    setup_requires="Cython",
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
    include_package_data=True,
    exclude_package_data={'': ['.git']},
    packages=find_packages("."),
    package_dir={"": "."},
    zip_safe=False)
