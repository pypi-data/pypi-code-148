from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappymongouser",
      version="1.5.1",
      description="Store Implementation for Users in MongoDB",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-py-mongo-user-store",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappymongouser"
      ],
      install_requires=[
            "pbu>=1.0.0",
            "pbumongo>=1.0.0"
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
