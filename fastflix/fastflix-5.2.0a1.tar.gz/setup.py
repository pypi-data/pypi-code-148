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
    'version': '5.2.0a1',
    'description': 'GUI Encoder',
    'long_description': '# FastFlix\n\n![preview](./docs/gui_preview.png)\n\nFastFlix is a simple and friendly GUI for encoding videos.\n\n[Download latest release from Github](https://github.com/cdgriffith/FastFlix/releases/latest)\n\nFastFlix keeps HDR10 metadata for x265, NVEncC HEVC, and VCEEncC HEVC, which will also be expanded to AV1 libraries when available.\n\nIt needs `FFmpeg` (version 4.3 or greater required, 5.0+ recommended) under the hood for the heavy lifting, and can work with a variety of encoders.\n\nJoin us on [discord](https://discord.gg/GUBFP6f)!\n\nCheck out [the FastFlix github wiki](https://github.com/cdgriffith/FastFlix/wiki) for help or more details, and please report bugs or ideas in the [github issue tracker](https://github.com/cdgriffith/FastFlix/issues)!\n\n#  Encoders\n\n## Software Encoders\n\n| Encoder   | x265 | x264 | rav1e | AOM AV1 | SVT AV1 | VP9 |\n|-----------|------|------|-------|---------|---------|-----|\n| HDR10     | ✓    |      |       |         | ✓       | ✓*  |\n| HDR10+    | ✓    |      |       |         |         |     |\n| Audio     | ✓    |  ✓   | ✓     | ✓       | ✓       | ✓   |\n| Subtitles | ✓    |  ✓   | ✓     | ✓       | ✓       |     |\n| Covers    | ✓    |  ✓   | ✓     | ✓       | ✓       |     |\n| bt.2020   | ✓    |   ✓  | ✓     | ✓       | ✓       | ✓   |\n\n## Hardware Encoders \n\nThese will require the appropriate hardware. Nvidia GPU for NVEnc, Intel GPU/CPU for QSVEnc, and AMD GPU for VCEEnc. \n\nMost of these are using [rigaya\'s hardware encoders](https://github.com/rigaya?tab=repositories) that must be downloaded separately, \nextracted to a directory of your choice, and then linked too in FastFlix Settings panel.\n\n### AV1\n\nTheis is only supported on the latest generation of graphics cards as of 2022, specifically the Intel Arc and Nvidia 4000 series. \n\n| Encoder   | [NVEncC AV1](https://github.com/rigaya/NVEnc/releases) | [QSVEncC AV!](https://github.com/rigaya/QSVEnc/releases) |\n|-----------|--------------------------------------------------------|----------------------------------------------------------|\n| HDR10     | ✓                                                      | ✓                                                        |\n| HDR10+    | ✓                                                      | ✓                                                        |\n| Audio     | ✓*                                                     | ✓*                                                       |\n| Subtitles | ✓                                                      | ✓                                                        |\n| Covers    |                                                        |                                                          |\n| bt.2020   | ✓                                                      | ✓                                                        |\n\n### HEVC / H.265\n\n| Encoder   | NVENC HEVC | [NVEncC HEVC](https://github.com/rigaya/NVEnc/releases) | [VCEEncC HEVC](https://github.com/rigaya/VCEEnc/releases) | [QSVEncC HEVC](https://github.com/rigaya/QSVEnc/releases) |\n|-----------|------------|---------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|\n| HDR10     |            | ✓                                                       | ✓                                                         | ✓                                                         |\n| HDR10+    |            | ✓                                                       | ✓                                                         | ✓                                                         |\n| Audio     | ✓          | ✓*                                                      | ✓*                                                        | ✓*                                                        |\n| Subtitles | ✓          | ✓                                                       | ✓                                                         | ✓                                                         |\n| Covers    | ✓          |                                                         |                                                           |                                                           |\n| bt.2020   | ✓          | ✓                                                       | ✓                                                         | ✓                                                         |\n\n### AVC / H.264\n\n| Encoder   | [NVEncC AVC](https://github.com/rigaya/NVEnc/releases) | [VCEEncC AVC](https://github.com/rigaya/VCEEnc/releases) | [QSVEncC AVC](https://github.com/rigaya/QSVEnc/releases) |\n|-----------|--------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|\n| HDR10     |                                                        |                                                          |                                                          |\n| HDR10+    |                                                        |                                                          |                                                          |\n| Audio     | ✓*                                                     | ✓*                                                       | ✓*                                                       |\n| Subtitles | ✓                                                      | ✓                                                        | ✓                                                        |\n| Covers    |                                                        |                                                          |                                                          |\n| bt.2020   | ✓                                                      | ✓                                                        | ✓                                                        |\n\n`✓ - Full support   |   ✓* - Limited support`\n\n\n\n\n# Releases\n\nView the [releases](https://github.com/cdgriffith/FastFlix/releases) for binaries for Windows, MacOS or Linux\n\nYou will need to have `ffmpeg` and `ffprobe` executables on your PATH and they must be executable. Version 4.3 or greater is required for most usage, latest master build is recommended and required for some features. The one in your package manager system may not support all encoders or options.\nCheck out the [FFmpeg download page for static builds](https://ffmpeg.org/download.html) for Linux and Mac.\n\n# Additional Encoders\n\nTo use rigaya\'s [Nvidia NVENC](https://github.com/rigaya/NVEnc/releases), [AMD VCE](https://github.com/rigaya/VCEEnc/releases), and [Intel QSV](https://github.com/rigaya/QSVEnc/releases) encoders, download them and extract them to folder on your hard drive. \n\nWindows: Go into FastFlix\'s settings and select the corresponding EXE file for each of the encoders you want to use. \n\nLinux: Install the rpm or deb and restart FastFlix\n\n\n## Running from source code\n\nRequires python3.8+\n\n```\ngit clone https://github.com/cdgriffith/FastFlix.git\ncd FastFlix\npython3 -m venv venv\n. venv/bin/activate\npip install -r requirements.txt\npython -m fastflix\n```\n\n# HDR\n\nOn any 10-bit or higher video output, FastFlix will copy the input HDR colorspace (bt2020). Which is [different than HDR10 or HDR10+](https://codecalamity.com/hdr-hdr10-hdr10-hlg-and-dolby-vision/).\n\n## HDR10\n\nFastFlix was created to easily extract / copy HDR10 data, which it can do with the above listed encoders (x265, NVEncC, VCEEncC, QSVEncC).\n\nVP9 has limited support to copy some existing HDR10 metadata, usually from other VP9 files. Will have the line "Mastering Display Metadata, has_primaries:1 has_luminance:1 ..." when it works.\n\nAV1 is still in development, and hopefully all encoder will support it in the future, but only SVT AV1 works through ffmpeg as of now for software encoders. \n\n* QSVEnc - Works! \n* NVEncC - Works!\n* rav1e -  can set mastering data and CLL via their CLI but [not through ffmpeg](https://github.com/xiph/rav1e/issues/2554).\n* SVT AV1 - Now supports HDR10 with latest master ffmpeg build, make sure to update before trying!\n* aomenc (libaom-av1) - does not look to support HDR10\n\n## HDR10+\n\nFor Windows users with dedicated graphics cards, the best thing to do is use a hardware encoder, as they all support HDR10+ currently!\n\nFastFlix also supports using generated or [extracted JSON HDR10+ Metadata](https://github.com/cdgriffith/FastFlix/wiki/HDR10-Plus-Metadata-Extraction) with HEVC encodes via x265. However, that is highly\ndependent on a FFmpeg version that has been compiled with x265 that has HDR10+ support. [BtbN\'s Windows FFmpeg builds](https://github.com/BtbN/FFmpeg-Builds) \nhave this support as of 10/23/2020 and may require a [manual upgrade](https://github.com/cdgriffith/FastFlix/wiki/Updating-FFmpeg).\n\nIf you add HDR10+ metadata file, make sure the encoding log does NOT contain the line `x265 [warning]: –dhdr10-info disabled. Enable HDR10_PLUS in cmake` or else it is unsupported. \n\n## HLG \n\nFastFlix (v4.0.2+) passes through HLG color transfer information to everything except webp and GIF. \n\n## Dolby Vision\n\nFastFlix does not plan to support Dolby Vision\'s proprietary format at this time.\n\n# Support FastFlix\n\nCheck out the different ways you can help [support FastFlix](https://github.com/cdgriffith/FastFlix/wiki/Support-FastFlix)!\n\n# License\n\nCopyright (C) 2019-2023 Chris Griffith\n\nThe code itself is licensed under the MIT which you can read in the `LICENSE` file. <br>\nRead more about the release licensing in the [docs](docs/README.md) folder. <br>\n\nCustom icons designed by Joey Catt | Onyx Studios\n\nEncoder icons for [VP9](https://commons.wikimedia.org/wiki/File:Vp9-logo-for-mediawiki.svg) and [AOM AV1](https://commons.wikimedia.org/wiki/File:AV1_logo_2018.svg) are from Wikimedia Commons all others are self created.\n\nAdditional button icons from [https://uxwing.com](https://uxwing.com)\n\nSample videos and thumbnail for preview image provided by [Jessica Payne](http://iamjessicapayne.com/)\n',
    'author': 'Chris Griffith',
    'author_email': 'chris@cdgriffith.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://fastflix.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
