from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
README = (this_directory / "README.md").read_text()

setup(
    name='DynamicHtml',
    packages=find_packages(exclude=("tests")),
    version='1.0.3',
    description='An extremely simple library used for gathering html from dynamic webpages using Pyppeteer.',
    url='https://github.com/commonkestrel/DynamicHtml',
    author='Kestrel',
    license='MIT',
    install_requires=['pyppeteer'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    python_requires='>= 3.4',
    test_suite='tests',
    long_description=README,
    long_description_content_type='text/markdown'
)