"""Setup.py for the apache-airflow-providers-couchbase package."""

from setuptools import find_namespace_packages, setup

version = "1.0.0"

with open("README.rst", "r",encoding='utf-8') as fh:
    long_description = fh.read()

def do_setup():
    """Perform the package apache-airflow-providers-couchbase setup."""
    setup(
        name='airflow-provider-couchbase',
        version=version,
        description='provide couchbase access through airflow.',
        long_description=long_description,
        url='https://github.com/aymen-ayadi/airflow-provider-couchbase',
        long_description_content_type='text/markdown',
        extras_require={},
        packages=find_namespace_packages(include=["airflow.providers.couchbase", "airflow.providers.couchbase.*"]),
    )


if __name__ == "__main__":
    do_setup()
