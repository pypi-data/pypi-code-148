from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PocketCRM',
    version='0.0.4',
    author='Russell Powers',
    author_email='russell@blackfoxx45.com',
    description='A simple CRM library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/BlackFoxgamingstudio/BDevManager2.git',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'numpy',
        'tk',
        
       
    ],
)
