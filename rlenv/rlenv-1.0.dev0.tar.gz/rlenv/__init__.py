"""Accenta Gym Environment

Note:

    This project is in beta stage.

Viewing documentation using IPython
-----------------------------------
To see which functions are available in `rlenv`, type ``rlenv.<TAB>`` (where
``<TAB>`` refers to the TAB key), or use ``rlenv.*get_version*?<ENTER>`` (where
``<ENTER>`` refers to the ENTER key) to narrow down the list.  To view the
docstring for a function, use ``rlenv.get_version?<ENTER>`` (to view the
docstring) and ``rlenv.get_version??<ENTER>`` (to view the source code).
"""

import rlenv.envs
import rlenv.sed
import rlenv.sed.wall
import rlenv.weather
import rlenv.weather.generator
import rlenv.weather.generator.brownianbridge
import rlenv.weather.generator.toysine
import rlenv.weather.generator.toysine2
import rlenv.weather.forecast
import rlenv.weather.forecast.bogus

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '1.0.dev0'

def get_version():
    return __version__

#__all__ = ['TODO']

# from rlenv.envs.registration import register

# register(
#     id='accenta-v0',
#     entry_point='rlenv.envs:AccentaEnv',
# )
