from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(name='senabase-starterpack',
      version='0.1.4',
      description='starterpack library',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Jungkyu Park',
      author_email='parkssie@gmail.com',
      url='https://github.com/parkssie/senabase-starterpack',
      python_requires='>=3.11',
      packages=find_packages("./", exclude=["prototypes"]),
      install_requires=[
          'psycopg2-binary>=2.9.*',
          'pyyaml>=6.*',
      ])
