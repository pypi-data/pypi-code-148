import os
import setuptools

import myacme
import myacme.__main__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    _long_description = f.read()

setuptools.setup(
    name         = 'myacme',
    version      = myacme.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'MyACME client library and command line tool',

    long_description = _long_description,
    long_description_content_type = 'text/markdown',

    url = 'https://declassed.art/repository/myacme',

    packages = [
        'myacme',
        'myacme/extras'
    ],

    entry_points = {
        'console_scripts': [
            'myacme=myacme.__main__:main',
            'myacme-zonefile=myacme.extras.zonefile:main'
        ]
    },

    install_requires=[
        'atomicwrites',
        'idna',
        'kvgargs',
        'pyyaml',
        'requests',
        'cryptography>=3.1'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Development Status :: 4 - Beta'
    ],

    python_requires = '>=3.7',
)
