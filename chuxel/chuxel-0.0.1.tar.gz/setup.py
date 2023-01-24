from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'chuxel'
LONG_DESCRIPTION = 'chuxel'

setup(
    name="chuxel",
    version=VERSION,
    author="hckmtrx",
    author_email="<hckmtrx@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'chuxel'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)