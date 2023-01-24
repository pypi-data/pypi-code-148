from setuptools import setup


setup(
  name='atonix',
  version='0.1.1',
  author='Kolton Stimpert',
  author_email='stimpertk@bv.com',
  description='A package, providing an easy to use interface for the AtonixOI web APIs.',
  platforms=['Python 3.9', 'Python 3.10', 'Python 3.11'],
  packages=['atonix'],
  install_requires=['cryptography>=37.0.1',
                    'setuptools>=61.2.0',
                    'requests>=2.27.1',
                    'openpyxl>=3.0.10',
                    'pandas>=1.5.2',
                    ],
)
