from distutils.core import setup
setup(
  name = 'TOPSIS-Devanshi-102053009',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-Devanshi-102053009'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Package for TOPSIS',   # Give a short description about your library
  author = 'Devanshi',                   # Type in your name
  author_email = 'ddevanshi60_be20@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/devanshi2545/topsis',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/devanshi2545/topsis/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'sklearn',
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
