from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'Relations of power in graphs'
LONG_DESCRIPTION = 'Given a directed graph, this Python package calculates the colonization matrix and properties such as hierarchy and mutualism.'

setup(
        name="power_sysGraph", 
        version=VERSION,
        author="Daniele De Luca",
        author_email="<prof.daniele.deluca@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "matplotlib", "numpy", "networkx", "graphviz"],
        
        keywords=['power', 'system of power', 'cooperation'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)