from setuptools import setup, find_packages

with open('requirements.txt') as f: 
    requirements = f.readlines() 
with open("README.md") as f:
 long_description = f.read()

setup(
    name='Topsis-Amit_Kumar-102003703',
    version='1.0.4',
    author='Amit Kumar',
    author_email='akumar11_be20@thapar.edu',
    description='A package -> Calculates Topsis Score and Rank them accordingly',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    license='MIT',
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'topsis=Topsis_Amit_Kumar.topsis:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords ='python package Amit Kumar', 
    install_requires = requirements, 
    zip_safe = False
)