from setuptools import setup
with open("readme.md", "r") as fh:
  long_description = fh.read()

setup(
  name='python-colorcode',
  version='0.3',
  author='Anshu Pal',
  author_email='anshupal257@gmail.com',
  packages=['python-colorcode'],
  description="A Python package for generating shades of a color",
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  install_requires=[
    'webcolors',
  ],
)
