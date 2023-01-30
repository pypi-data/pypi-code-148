
#! /usr/bin/env python
#
# Copyright (C) 2020 wsn-toolkit
#
# This program was written by Edielson P. Frigieri <edielsonpf@gmail.com>
#               
# License: MIT
#version = attr: wsntk.__version__


import setuptools

if __name__ == '__main__':
    setuptools.setup(
		setup_requires=['pytest-runner', 'pbr'],
		pbr=True,
		tests_require=['pytest'],
    )
	