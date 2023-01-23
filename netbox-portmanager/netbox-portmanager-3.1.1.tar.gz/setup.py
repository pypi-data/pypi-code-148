from setuptools import setup, find_packages


setup(
    name='netbox-portmanager',
    version='3.1.1',
    license='MIT',
    author="Michal Drobny",
    author_email='drobny@ics.muni.cz',
    packages=find_packages('portmanager'),
    package_dir={'': 'portmanager'},
    url='',
    include_package_data=True,
    keywords='netbox portmanager',
    install_requires=[
        'pysnmp'
    ],
)
