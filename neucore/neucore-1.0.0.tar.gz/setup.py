import setuptools
from distutils.core import setup

setup(name='neucore',
      version='1.0',
      description='Ailiverse API Package',
      author='Nicholas Chua, Burhan Ul Tayyab',
      author_email='nicholas@ailiverse.com, burhan@ailiverse.com',
      url='https://ailiverse.com',
      packages=['neucore'],
      install_requires=[
          "requests",
          "tqdm",
          "yaspin",
          "requests_toolbelt"
      ],
      package_dir = {'neucore': 'src/neucore'}
     )


