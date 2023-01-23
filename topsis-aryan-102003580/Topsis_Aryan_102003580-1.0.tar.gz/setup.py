
from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name = 'Topsis_Aryan_102003580',         # How you named your package folder (MyLib)
  packages = ['Topsis_Aryan_102003580'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A topsis package',
     # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Aryan Sharma',                   # Type in your name
  author_email = 'aryansharma5669@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aryansharma56/topsis',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aryansharma56/topsis',    # I explain this later on
  keywords = ['Aryan', 'Topsis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'panda',
          'numpy'

      ],
  
)