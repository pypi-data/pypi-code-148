from setuptools import setup
import re


with open('hypixel_data/__init__.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE
    ).group(1)

with open('README.md') as f:
    readme = f.read()

classifiers = [
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',
    'Natural Language :: English',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='hypixel.py-data',
    author='duhby',
    license='MIT',
    version=version,
    description='A Python package for optional, extra data used with the hypixel.py library',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/duhby/hypixel.py-data',
    classifiers=classifiers,
    python_requires='>=3.8',
)
