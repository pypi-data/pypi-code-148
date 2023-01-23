from setuptools import setup, find_packages

setup(
    name="whatistheanswer",
    version="0.0.1",
    description="Say Hello",
    packages=find_packages(),
    install_requires=['elasticsearch==7.13.1'],
)