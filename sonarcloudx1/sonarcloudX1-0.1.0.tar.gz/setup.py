from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sonarcloudX1',  # Required
    version='0.1.0',  # Required
    author="Carlos Henrique Maulaz de Freitas",
    author_email="carlosmaulaz@gmail.com",
    description="lib para buscar wrapper SonarCloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/immigrant-data-driven-development/libs/application/sonarcloud.git",
    packages=find_packages(),
    
    install_requires=[
        'python-sonarqube-api',
        'factory-boy'
    ],

    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    setup_requires=['wheel'],
    
)


