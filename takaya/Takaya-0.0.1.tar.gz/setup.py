from setuptools import setup,find_packages
setup(
  name = 'Takaya',         # How you named your package folder (MyLib)
  packages=find_packages(),  # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'YOU CAN REVERSE,REMOVE AND COUNT VOWELS IN THE STRING',   # Give a short description about your library
  author = 'SASHIN',                   # Type in your name
  author_email = 'sashin_ranjitkar@takaya.co.jp',      # Type in your E-Mail
#   url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['REVERSE', 'REMOVE', 'VOWEL_COUNT'],   # Keywords that define your package best
  requires=[],
)