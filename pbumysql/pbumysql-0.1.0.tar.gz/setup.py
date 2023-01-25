from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pbumysql",
      version="0.1.0",
      description="Basic MySQL wrapper for object-oriented collection handling",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/pbu-mysql",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      license="Apache-2.0",
      packages=[
          "pbumysql"
      ],
      install_requires=[
          "mysql-connector-python",
          "tzlocal",
          "pbu>=1.0.0",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
