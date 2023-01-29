from distutils.core import setup
__authors__  = 'Damian Guenzing'

__version__ = '0.0.4'


setup(
  name = 'assaypy',
  packages = ['assaypy'],
  version = __version__,
  license='MIT',        
  description = 'package for analysis of experimental assay data',
  author = __authors__,
  author_email = 'gnzng@protonmail.ch',
  url = 'https://github.com/gnzng/',
  keywords = ['assay'],
  install_requires=[ 
          'numpy',
          'pandas',
          'scipy',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
  ],
)