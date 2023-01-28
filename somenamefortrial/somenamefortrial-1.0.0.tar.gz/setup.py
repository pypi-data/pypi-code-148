from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
]

setup(
    name = 'somenamefortrial',
    version = '1.0.0',
    description = 'A helper module for recsys',
    long_description= open('README.txt').read()+ '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'HU Researchers',
    author_email='sis.rs6.2022@gmail.com',
    license='MIT',
    classifiers = classifiers,
    keywords = 'helper',
    packages=find_packages(),
    install_requires = ['pandas']
)
