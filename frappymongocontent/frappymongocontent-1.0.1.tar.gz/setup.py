from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappymongocontent",
      version="1.0.1",
      description="Store Implementation for Content in MongoDB",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-py-mongo-content-store",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappymongocontent"
      ],
      install_requires=[
            "pbumongo>=1.0.0",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
