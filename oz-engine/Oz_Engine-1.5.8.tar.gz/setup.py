from setuptools import setup

with open("readme.md", "r") as fh:
  long_description = fh.read()

setup(
  name = "Oz_Engine",
  version = "1.5.8",
  description = "A module for text based games",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = None,
  author = "SplatCraft",
  author_email = "splatcraft.5972@gmail.com",
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "GNU General Public License v3 (GPLv3)",
  packages=["OzEngine"],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.1",
)