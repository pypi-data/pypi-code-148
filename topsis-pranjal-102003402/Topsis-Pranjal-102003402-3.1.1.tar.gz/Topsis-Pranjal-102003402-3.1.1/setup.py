from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Topsis-Pranjal-102003402',
  version='3.1.1',
  description='TOPSIS - Technique for Order of Preference by Similarity to Ideal Solution - By Pranjal Arora 102003402',
  long_description=open('Readme.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/pranjal-arora/Topsis',  
  author='Pranjal Arora',
  author_email='prv.gma@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOPSIS', 
  packages=find_packages(),
  install_requires=[''] 
)