from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-XiaomiScale',
      version='0.2.1',
      description='CraftBeerPi4 Xiaomi Scale integration plugin',
      author='Guy Lev',
      author_email='guyparis94@gmail.com',
      url='https://github.com/madhatguy/cbpi4-XiaomiScale',
      download_url='https://github.com/madhatguy/cbpi4-XiaomiScale/archive/refs/heads/master.zip',
      install_requires=['scapy >= 2.4.5'],
      license='GPLv3',
      include_package_data=True,
      package_data={
          # If any package contains *.txt or *.rst files, include them:
          '': ['*.txt', '*.rst', '*.yaml'],
          'cbpi4-XiaomiScale': ['*', '*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-XiaomiScale'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
