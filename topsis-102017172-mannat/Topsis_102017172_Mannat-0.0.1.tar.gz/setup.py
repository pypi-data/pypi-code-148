from distutils.core import setup

setup(
  name = 'Topsis_102017172_Mannat',
  packages = ['Topsis_102017172_Mannat'],
  version = '1.0.0',  
  license='MIT', 
  description = 'Topsis score calculator',
  long_description=open("README.md").read(),
  author = 'Mannat',
  author_email = 'mannat7873@gmail.com',
  url = 'https://github.com/Mannat7/Topsis_102017172',
  keywords = ['topsis', 'rank', 'topsis score'], 
  install_requires=["pandas"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
  package_dir={'':"src"}
)