
from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name = 'Topsis_Rakshika_102003624',         # How you named your package folder (MyLib)
  packages = ['Topsis_Rakshika_102003624'],   # Chose the same as "name"
  version = '0.13',      # Start with a small number and increase it with every change you make
  license='MIT',        
     # Give a short description about your library
  long_description="Topsis",
  long_description_content_type="text/markdown",
  author = 'Rakshika',                   # Type in your name
  author_email = 'vatsrakshika@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aryansharma56/topsis',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rakshika/topsis',    # I explain this later on
  keywords = ['Rakshika', 'Topsis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'panda',
          'numpy'

      ],
  
)