from setuptools import setup

setup(name='augmolino',
      packages=['augmolino'],
      version='0.0.2a',
      description='augmentation for audio based datasets for machine learning',
      url='https://github.com/jake-is-ESD-protected/augmolino',
      download_url="https://github.com/jake-is-ESD-protected/augmolino/archive/refs/tags/0.0.2.tar.gz",
      author='Jakob Tschavoll',
      author_email='jt@tschavoll.at',
      license='GPL 3.0',
      classifiers=[],
      keywords=["ML", "augmentation", "audio"],
      zip_safe=False,
      install_requires=[
          'numpy',
          'scipy',
          'librosa',
          'soundfile'])
