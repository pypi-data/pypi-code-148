from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'A2G Runner for Local Workflow'
LONG_DESCRIPTION = 'Package that enables users to run user_fx on a local environment as it was run on A2G.IO'

with open('requirements.txt') as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="a2grunner",
    version=VERSION,
    author="Carlos Alvarado",
    author_email="<carlos@alert2gain.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires = required,

    keywords=['python', 'a2g base-a2grunner'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)