from distutils.core import setup
setup(
  name = 'ISSAstronaut_Tracker',         # How you named your package folder (MyLib)
  packages = ['ISSAstronaut_Tracker'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A tracker to tack the ISS, and report which astronauts are on it.',   # Give a short description about your library
  author = 'SOMERANDOMDUDEEEEEEE',                   # Type in your name
  author_email = 'abhimanyu.daripally@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/SOMERANDOMDUDEEEEEEE/ISSTracker',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Astronaut', 'Tracker', 'ISS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'json',
          'urllib.request',
	  'turtle',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',
  ],
)
