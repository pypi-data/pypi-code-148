from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Topsis-Madhurya-102003407',
  version='0.0.1',
  description='A package to Implement Topsis Model',
  long_description=open('Readme.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Madhurya Peram',
  author_email='nperam_be20@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOPSIS', 
  packages=find_packages(),
  install_requires=[''] 
)