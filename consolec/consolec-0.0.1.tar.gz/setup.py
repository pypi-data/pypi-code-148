#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: two-it2022
:copyright: (c) 2022 two-it2022
"""

version = '0.0.1'
'''
with open('__readme__.md', encoding='utf-8') as f:
      long_description = f.read()
'''

long_description = '''
Consolec
Created for create tables, colors and more in console.
'''


setup(
      name='consolec',
      version=version,

      author='two-it2022',
      author_email='kodland.group@gmail.com',

      description=(
            u'Python module for work in console'
            u'Two It 2022'
      ),
      long_description=long_description,
      #long_description_content_type='text/markdown',

      url='https://github.com/TwoIt202/Consolec',
      download_url='https://github.com/TwoIt202/Consolec/raw/6d7c5fe31c881bf59619e9e2879cbf83fb4504e4/consolec.zip'.format(
            version
      ),


      packages=['consolec'],
      install_requires=['termcolor', 'prettytable'],

      classifiers=[
            'Operating System :: OS Independent',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11'
      ]

)