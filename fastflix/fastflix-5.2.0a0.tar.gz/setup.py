# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastflix',
 'fastflix.encoders',
 'fastflix.encoders.av1_aom',
 'fastflix.encoders.avc_x264',
 'fastflix.encoders.common',
 'fastflix.encoders.copy',
 'fastflix.encoders.ffmpeg_hevc_nvenc',
 'fastflix.encoders.gif',
 'fastflix.encoders.h264_videotoolbox',
 'fastflix.encoders.hevc_videotoolbox',
 'fastflix.encoders.hevc_x265',
 'fastflix.encoders.nvencc_av1',
 'fastflix.encoders.nvencc_avc',
 'fastflix.encoders.nvencc_hevc',
 'fastflix.encoders.qsvencc_av1',
 'fastflix.encoders.qsvencc_avc',
 'fastflix.encoders.qsvencc_hevc',
 'fastflix.encoders.rav1e',
 'fastflix.encoders.svt_av1',
 'fastflix.encoders.svt_av1_avif',
 'fastflix.encoders.vceencc_av1',
 'fastflix.encoders.vceencc_avc',
 'fastflix.encoders.vceencc_hevc',
 'fastflix.encoders.vp9',
 'fastflix.encoders.webp',
 'fastflix.models',
 'fastflix.widgets',
 'fastflix.widgets.panels',
 'fastflix.widgets.windows']

package_data = \
{'': ['*'],
 'fastflix': ['data/*',
              'data/encoders/*',
              'data/icons/*',
              'data/icons/black/*',
              'data/icons/selected/*',
              'data/icons/white/*',
              'data/rotations/*',
              'data/styles/breeze_styles/dark/*',
              'data/styles/breeze_styles/light/*',
              'data/styles/breeze_styles/onyx/*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'chardet>=5.1.0,<5.2.0',
 'colorama>=0.4,<1.0',
 'coloredlogs>=15.0,<16.0',
 'iso639-lang==0.0.9',
 'mistune>=2.0,<3.0',
 'pathvalidate>=2.4,<3.0',
 'psutil>=5.9,<6.0',
 'pydantic>=1.9,<2.0',
 'pyside6>=6.3,<7.0',
 'python-box[all]>=6.0,<7.0',
 'requests>=2.28,<3.0',
 'reusables>=0.9.6,<0.10.0']

entry_points = \
{'console_scripts': ['fastflix = fastflix.__main__:start_fastflix']}

setup_kwargs = {
    'name': 'fastflix',
    'version': '5.2.0a0',
    'description': 'GUI Encoder',
    'long_description': 'None',
    'author': 'Chris Griffith',
    'author_email': 'chris@cdgriffith.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
