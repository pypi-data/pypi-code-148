from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappyflaskdataset",
      version="1.3.3",
      description="Flask Endpoints for Data Set Management and Retrieval",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-flask-datasets",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappyflaskdataset"
      ],
      install_requires=[
            "flask",
            "pbu>=1.0.0",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
