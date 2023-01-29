from setuptools import setup, find_packages


BEAUTIFUL_PACKAGE_NAME = 'Pyhandling'
PACKAGE_NAME = 'pyhandling'

VERSION = '2.2.0'

REQUIRES = ('pyannotating==1.2.1', )

with open('README.md') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name=BEAUTIFUL_PACKAGE_NAME,
    description="Library for metaprogramming",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license_files = ('LICENSE',),
    license='GNU General Public License v3.0',
    version=VERSION,
    install_requires=REQUIRES,
    url="https://github.com/TheArtur128/Pyhandling",
    download_url=f"https://github.com/TheArtur128/Pyhandling/archive/refs/tags/v{VERSION}.zip",
    author="Arthur",
    author_email="s9339307190@gmail.com",
    python_requires='>=3.11',
    classifiers=['Programming Language :: Python :: 3.11'],
    keywords=[
        "syntax", "library", "utils", "logging", "metaprogramming",
        "annotations", "immutability", "data-structures", "error-handling",
        "handling", "checking", "utils-library", "pseudo-operators"
    ],
    packages=find_packages()
)