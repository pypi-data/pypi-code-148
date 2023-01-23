from distutils.core import setup
setup(
  name = 'TOPSIS_Ananya_102003124',         #Name of package folder
  packages = ['TOPSIS_Ananya_102003124'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package is implimentation of multi-criteria decision analysis using topsis',   # Give a short description about your library
  author = 'Ananya Malik',                   # Type in your name
  author_email = 'ananyamalik09@gmail.com',      #E-Mail
  url = 'https://github.com/ananyamalik09/TOPSIS_Ananya_102003124',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ananyamalik09/TOPSIS_Ananya_102003124/archive/refs/tags/v_0.1.tar.gz',   
  keywords = ['topsis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          ''
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