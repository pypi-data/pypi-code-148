import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="simple-transfer",
    author="Henry Jones",
    author_email="henryivesjones@gmail.com",
    url="https://github.com/henryivesjones/simple-transfer",
    description="A tool for moving data between relational databases.",
    packages=["simple_transfer", "simple_transfer.connections"],
    package_dir={
        "simple_transfer": "simple_transfer",
        "simple_transfer.connections": "simple_transfer/connections",
    },
    package_data={
        "simple_transfer": ["py.typed"],
        "simple_transfer.connections": ["py.typed"],
    },
    include_package_data=True,
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
    ],
)
