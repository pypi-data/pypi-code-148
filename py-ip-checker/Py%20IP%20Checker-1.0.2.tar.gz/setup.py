from setuptools import setup

readme = open('README.md', 'r', encoding='utf-8').read()

setup(name='Py IP Checker',
	version='1.0.2',
	description='Get IP data',
	packages=['src'],
	author_email='zukovlesa0@gmail.com',
	zip_safe=False,
	long_description=readme)