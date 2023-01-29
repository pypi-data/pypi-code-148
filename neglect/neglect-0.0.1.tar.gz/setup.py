from setuptools import setup
import setuptools
with open("README.md","r")as fh:
 long_description=fh.read()

setup(
     name='neglect',
  version='0.0.1',
  description='Neglecting usage of Exceptional handling in Python',
  author='Vishal R',
 long_description=long_description,
 long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  keywords=['neglect','NEGLECT','neglect try except','ignore','omit','neglect exceptional handling'],
  classifiers=[
   "Programming Language :: Python :: 3",
   "License :: OSI Approved :: MIT License",
   "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  py_modules=['neglect'],
  package_dir={'':'src'},


 )