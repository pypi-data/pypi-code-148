from setuptools import setup


VERSION = '0.0.1a0'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sortme',
    description='Sort Me API wrapper for Python. Automate with a bang!',

    long_description=long_description,
    long_description_content_type='text/markdown',

    version=VERSION,
    license='MIT',
    author="Sort Me",
    author_email='guys@sort-me.org',
    packages=["sortme", "sortme.groups"],
    url='https://github.com/sort-me/python-api',
    keywords='sort-me.org sort-me sortme api sort_me sort me codeforces',
    install_requires=[
        'requests',
        'dacite'
    ],
)