from setuptools import setup, find_packages


setup(
    name='netbox-portmanager',
    version='3.1',
    license='MIT',
    author="Michal Drobny",
    author_email='drobny@ics.muni.cz',
    packages=find_packages('portmanager'),
    package_dir={'': 'portmanager'},
    url='',
    keywords='netbox portmanager',
    install_requires=[
        'pysnmp'
    ],
)
