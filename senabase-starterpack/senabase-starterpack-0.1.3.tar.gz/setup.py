from setuptools import setup, find_packages

setup(name='senabase-starterpack',
      version='0.1.3',
      description='SENABASE Starterpack',
      author='Jungkyu Park',
      author_email='parkssie@gmail.com',
      url='https://github.com/parkssie/senabase-starterpack',
      python_requires='>=3.11',
      packages=find_packages("./", exclude=["prototypes"]),
      install_requires=[
          'psycopg2-binary>=2.9.*',
          'pyyaml>=6.*',
      ])
