# Create complete setup.py file for Topsis-Anant-102003755 package

from setuptools import setup

setup(
    name='topsisAnant102003755',
    version='0.0.6',
    description='Topsis Score Calculator',
    long_description='Command line tool and python package to calculate topsis score of a dataset',
    long_description_content_type='text/markdown',
    url="https://github.com/amish-1729/Topsis-Anant-102003755",
    author='Anant Mishra',
    author_email='amishra_be20@thapar.edu',
    license='MIT',
    packages=['topsis'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['topsis=topsis.topsis:main'],
    },
    install_requires = ['pandas','numpy','openpyxl','tabulate'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

)


