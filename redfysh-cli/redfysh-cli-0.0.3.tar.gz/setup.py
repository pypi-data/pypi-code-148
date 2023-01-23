import os

from setuptools import setup, find_packages

# reading long description from file
with open('README.md') as file:
    long_description = file.read()


# specify requirements of your package here
with open("requirements.txt") as file:
    REQUIREMENTS = file.readlines()

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

version = os.environ.get("CI_COMMIT_TAG", '0.0.1')

# calling the setup function
setup(name='redfysh-cli',
      version=version,
      description='The CLI to use with your Redfysh Account',
      long_description=long_description,
      url='https://gitlab.com/bdonnell/redfish/cli',
      author='Ben Donnelly',
      author_email='ben@redfysh.com',
      license='Apache 2.0',
      license_files=['LICENSE.txt', 'NOTICE.txt'],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'redfysh = redfysh_cli.cli:main'
          ]
      },
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='redfysh test testing',
      )
