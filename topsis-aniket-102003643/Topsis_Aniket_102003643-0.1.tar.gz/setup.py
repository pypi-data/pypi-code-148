from setuptools import setup
def readme():
  with open('README.md')as f:
    README = f.read()
  return README

setup(
  name = 'Topsis_Aniket_102003643',         # How you named your package folder (MyLib)
  packages = ['Topsis_Aniket_102003643'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'It is a topsis package.',   # Give a short description about your library
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Aniket Sharma',                   # Type in your name
  author_email = 'anikets1023@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Aniket-Sharma27/Topsis_Aniket_102003643',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Aniket-Sharma27/Topsis_Aniket_102003643/archive/refs/tags/0.1.tar.gz',    # I explain this later on
  keywords = ['MCDM', '102003643', 'TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    
    ],
 )