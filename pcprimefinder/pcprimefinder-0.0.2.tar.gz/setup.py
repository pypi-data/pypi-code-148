from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='pcprimefinder',
  version='0.0.2',
  description='A faster way to find if a number is prime',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Prathamesh Chavan',
  author_email='pratham.chavan28@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='prime,maths',
  packages=find_packages(),
  install_requires=['']
)
