from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
  name = 'topsis_17188',         # How you named your package folder (MyLib)
  packages = ['topsis_17188'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python Package implementing TOPSIS method for multi-criteria decision making method',   # Give a short description about your library
  long_description= readme(),
  long_description_content_type='text/markdown',
  author = 'Kanuj Boora',                   # Type in your name
  author_email = 'boorakanuj@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/kanuj-boora/topsis-17188',   # Provide either the link to your github or to your website
  keywords = ['topsis', 'mcdm', 'mcda', 'TIET', 'thapar'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
      ],
  entry_points={
        'console_scripts': [
            'topsis=topsis_17188.topsis:main'
        ]
    },
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