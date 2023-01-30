from setuptools import setup

setup(
	name='m0deler-python',
	version='0.2',
	author='Chainhaus',
	packages=['m0deler'],
	install_requires=[
		'pandas',
		'matplotlib',
		'datetime',
		'requests',
		'numpy',
		'chart_studio',
        'plotly',

	],
	include_package_data=True,
)