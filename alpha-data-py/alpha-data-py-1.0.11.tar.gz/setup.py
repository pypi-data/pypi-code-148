from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='alpha-data-py',
    version='1.0.11',
    packages=['adata'],
    url='https://gitlab.com/alphaticks/alpha-data-py',
    license='copyright',
    author='Alphaticks',
    description='client to communicate with alphaticks',
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[
        'alpha-public-registry-grpc==1.0.3',
        'tickstore-python-client==1.0.2'
    ]
)
