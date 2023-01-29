from setuptools import setup, find_packages

setup(
    name = 'qonic',
    packages = ['qonic', 'qonic.ConstraintSatisfaction', 'qonic.QProgram'],
    version = '0.0.8',
    description = 'The Qonic project is an open source, expandable framework for solving problems using hybrid quantum computing solutions.',
    author = 'cogrpar',
    author_email = 'owen.r.welsh@hotmail.com',
    url = 'https://github.com/Qonic-Team/qonic.git',
    download_url = 'https://github.com/Qonic-Team/qonic/archive/refs/heads/main.zip',
    license='Apache License 2.0',
    keywords = ['qonic', 'quantum computing'],
    setup_requires=['wheel'],
    install_requires=['numpy>=1.19.2', 'sympy>=1.11', 'PyYAML>=5.4.1', 'tequila-basic>=1.8.1', 'qiskit>=0.21.2', 'forest-benchmarking>=0.8.0', 'dimod>=0.11.5', 'dwavebinarycsp>=0.2.0']
)
