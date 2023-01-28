from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(name='Py IP Checker',
	version='1.0.0',
	description='Get IP data',
	packages=['src'],
	author_email='zukovlesa0@gmail.com',
	zip_safe=False,
	long_description=readme)