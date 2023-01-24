import codecs
import os
from distutils.core import setup

from setuptools import find_packages

setup_path = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(setup_path, 'README.md'), encoding='utf-8-sig') as f:
    README = f.read()

setup(name='infodeslib',
      version='0.0.3',
      url='https://github.com/fukashi-hatake/infodeslib',
      maintainer='Firuz Juraev',
      maintainer_email='f.i.juraev@gmail.com',
      description='Implementation of Dynamic Ensemble Selection methods for Late Fusion',
      long_description=README,
      author='Firuz Juraev',
      author_email='f.i.juraev@gmail.com',
      license='BSD 3-clause "New" or "Revised License"',

      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      install_requires=[
          'scikit-learn>=0.21.0',
          'numpy>=1.17.0',
          'scipy>=1.4.0',
      ],
      python_requires='>=3',      

      packages=find_packages())
