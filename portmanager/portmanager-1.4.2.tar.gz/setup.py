from setuptools import find_packages, setup

setup(
    name='portmanager',
    version='1.4.2',
    description='Netbox Portmanager',
    long_description='Netbox Portmanager',
    url='https://github.com/dansheps/netbox-secretstore/',
    download_url='https://www.pypi.org/project/netbox-secretstore/',
    author='Michal Drobny',
    author_email='ddrobny@ics.muni.cz',
    license='Apache 2.0',
    install_requires=[
        'pysnmp'
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)