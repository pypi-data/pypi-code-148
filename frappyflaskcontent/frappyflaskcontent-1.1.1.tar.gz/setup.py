from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappyflaskcontent",
      version="1.1.1",
      description="Flask Endpoints for Content Management and Retrieval",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-flask-content",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappyflaskcontent"
      ],
      install_requires=[
            "flask",
            "pbu>=1.0.0",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
