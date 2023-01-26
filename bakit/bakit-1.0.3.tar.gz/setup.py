from setuptools import setup, find_packages

# README.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
   readme = readme_file.read()

setup(
   name='bakit',
   packages=find_packages(),
   version="1.0.3",
   description='BAKit Provides Python Built-in better alternatives',
   author='Nawaf Alqari',
   author_email='nawafalqari13@gmail.com',
   keywords=['events', 'event', 'bakit', 'pyevent'],
   long_description=readme,
   long_description_content_type='text/markdown',
   project_urls={
      'Documentation': 'https://github.com/nawafalqari/bakit#readme',
      'Bug Tracker': 'https://github.com/nawafalqari/bakit/issues',
      'Source Code': 'https://github.com/nawafalqari/bakit/',
      'Discord': 'https://discord.gg/cpvynqk4XT'
   },
   license='MIT',
   url='https://github.com/nawafalqari/bakit/',
   classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
    ],
)