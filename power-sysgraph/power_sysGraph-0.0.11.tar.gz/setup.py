from setuptools import setup, find_packages

VERSION = '0.0.11' 
DESCRIPTION = 'Relations of power in graphs'

setup(
        name="power_sysGraph", 
        version=VERSION,
        author="Daniele De Luca",
        author_email="<prof.daniele.deluca@gmail.com>",
        description=DESCRIPTION,
        readme = "README.md",
        packages=find_packages(),
        install_requires=["numpy", "matplotlib", "numpy", "networkx", "graphviz"],
        keywords=['power', 'system of power', 'cooperation'],
        classifiers= [
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ]
)