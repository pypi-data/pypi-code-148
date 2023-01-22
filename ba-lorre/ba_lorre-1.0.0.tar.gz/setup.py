from setuptools import setup, find_packages

VERSION = '1.0.0'

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='ba_lorre',
    version=VERSION,
    description='A Python implementation of the Bees Algorithm based Local Optima Region Radius Extimator (BA-LORRE). This library allows an out-of-the-box use of the numerical optimisation algorithm on an user-defined target function. The algorithm can be configured to find the maxima of the target function with an iterative process.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='GNUv3',
    packages=['ba_lorre'],
    author='Luca Baronti',
    author_email='lbaronti@gmail.com',
    keywords=['Optimisation', 'Optimization', 'Bees Algorithm', 'Intelligent Optimisation', 'LORRE'],
    url='https://gitlab.com/luca.baronti/ba_lorre',
    download_url='https://pypi.org/project/ba_lorre/',
		classifiers=[
			# How mature is this project? Common values are
			'Development Status :: 5 - Production/Stable',
			# Indicate who your project is intended for
			'Intended Audience :: Education',
			'Intended Audience :: Science/Research',
			'Topic :: Scientific/Engineering :: Mathematics',
			# Pick your license as you wish (should match "license" above)
			'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
			# Specify all Python versions you support here.
			'Programming Language :: Python :: 3',
		]
)

install_requires = [ ]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=False)
