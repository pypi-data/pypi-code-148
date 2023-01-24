from setuptools import setup, find_packages

setup(
    name='netsuite-python',
    version='1.0.0',
    description='Python SDK for Netsuite API with Django Integration',
    url='https://bitbucket.org/theapiguys/netsuite-python',
    author='Will @ TheAPIGuys',
    author_email='will@theapiguys.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'jwt',
        "urllib3 >= 1.15",
        "six >= 1.10",
        "certifi",
        "python-dateutil"
    ],
    entry_points={
        'console_scripts': [
            'netsuite = netsuite.scripts.cli:cli',
        ],
    },
)
