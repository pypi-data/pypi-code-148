# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soundbridgefx']

package_data = \
{'': ['*'],
 'soundbridgefx': ['web/client/*',
                   'web/client/_app/*',
                   'web/client/_app/immutable/*',
                   'web/client/_app/immutable/assets/*',
                   'web/client/_app/immutable/chunks/*',
                   'web/client/_app/immutable/components/pages/*',
                   'web/client/_app/immutable/components/pages/ledfx/*',
                   'web/client/_app/immutable/components/pages/settings/*',
                   'web/client/_app/immutable/components/pages/stream/*',
                   'web/client/_app/immutable/modules/pages/*',
                   'web/prerendered/pages/*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'flask-cors>=3.0.10,<4.0.0',
 'flask>=2.2.2,<3.0.0',
 'jsonpickle>=3.0.1,<4.0.0',
 'ledfx>=2.0.60,<3.0.0',
 'soco>=0.28.1,<0.29.0',
 'soundcard>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['soundbridgefx = soundbridgefx.__main__:main']}

setup_kwargs = {
    'name': 'soundbridgefx',
    'version': '0.2.0b0',
    'description': '',
    'long_description': '# SoundBridge\nSpotify LedFx Sonos Proxy\n\n## About\n\nThis project tries to make an Spotify LedFX Sonos proxy, meaning it will show up as an spotify connect device allowing you to stream music to this device.\nThen the "proxy" part will kick in and will get the incoming spotify audio to both ledfx and a sonos device of your chosing, allowing you to headless hear and see your music.\n\nCurrently WIP',
    'author': 'Martyn van Dijke',
    'author_email': 'martijnvdijke600@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/martynvdijke/SoundBridgeFx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
