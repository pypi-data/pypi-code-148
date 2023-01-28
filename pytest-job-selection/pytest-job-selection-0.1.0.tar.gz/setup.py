#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-job-selection',
    version='0.1.0',
    author='Arvid Jakobsson',
    author_email='arvid.jakobsson@nomadic-labs.com',
    maintainer='Arvid Jakobsson',
    maintainer_email='arvid.jakobsson@nomadic-labs.com',
    license='MIT',
    url='https://gitlab.com/arvidnl/pytest-job-selection',
    description='A pytest plugin for load balancing test suites',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['pytest_job_selection'],
    python_requires='>=3.5',
    install_requires=[
        'pytest>=3.5.0',
        'typing_extensions>=4.4.0',
    ],
    extras_require={
        'dev': [
            'cram>=0.6',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'job-selection = pytest_job_selection',
        ],
        'console_scripts': [
            'glci_jobs_fetch_reports = scripts.jobs_fetch_reports:main',
        ],
    },
)
